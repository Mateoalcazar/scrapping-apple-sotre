import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time
import json

class AppStoreKeywordScraper:
    def __init__(self):
        self.base_url = "https://itunes.apple.com/search"
        self.suggestion_url = "https://search.itunes.apple.com/WebObjects/MZSearchHints.woa/wa/hints"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }

    def get_search_suggestions(self, term: str, country: str = "US"):
        params = {
            "media": "software",
            "term": term,
            "country": country,
            "version": "2"
        }
        try:
            response = requests.get(
                self.suggestion_url, 
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            # Validar que la respuesta es JSON válido
            try:
                data = response.json()
                if isinstance(data, dict) and "terms" in data:
                    return [suggestion["term"] for suggestion in data["terms"]]
                else:
                    st.warning(f"Invalid response format for term '{term}'")
                    return [term]  # Return original term if no suggestions
            except json.JSONDecodeError:
                st.warning(f"Invalid JSON response for term '{term}'")
                return [term]
                
        except requests.exceptions.RequestException as e:
            st.warning(f"Error getting suggestions for {term}: {str(e)}")
            return [term]  # Return original term if request fails

    def get_app_data(self, keyword: str, country: str = "US"):
        params = {
            "term": keyword,
            "country": country,
            "media": "software",
            "limit": 200
        }
        try:
            response = requests.get(
                self.base_url, 
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            st.warning(f"Error getting app data for {keyword}: {str(e)}")
            return []

    def analyze_keywords(self, initial_terms, country="US"):
        all_keywords = set()
        keyword_data = []

        with st.spinner('Getting keyword suggestions...'):
            # First get suggestions
            for term in initial_terms:
                suggestions = self.get_search_suggestions(term, country)
                if suggestions:  # Only add if we got valid suggestions
                    all_keywords.update(suggestions)
                all_keywords.add(term)
                time.sleep(1)  # Respect rate limits

        total = len(all_keywords)
        if total == 0:
            st.error("No keywords to analyze!")
            return pd.DataFrame()

        with st.spinner('Analyzing apps...'):
            progress_bar = st.progress(0)
            
            # Then analyze each keyword
            for i, keyword in enumerate(all_keywords):
                progress_bar.progress((i + 1) / total)
                
                apps = self.get_app_data(keyword, country)
                if apps:
                    keyword_data.append({
                        'keyword': keyword,
                        'num_apps': len(apps),
                        'avg_rating': sum(app.get('averageUserRating', 0) for app in apps) / len(apps) if apps else 0,
                        'total_ratings': sum(app.get('userRatingCount', 0) for app in apps),
                        'date_collected': datetime.now().strftime('%Y-%m-%d')
                    })
                time.sleep(1)

        return pd.DataFrame(keyword_data)

def main():
    st.title("App Store Keyword Analysis 📱")
    
    with st.sidebar:
        st.header("Configuration")
        
        country_options = {
            "United States": "US",
            "United Kingdom": "GB",
            "Spain": "ES",
            "France": "FR",
            "Germany": "DE"
        }
        
        selected_country = st.selectbox(
            "Select Country",
            options=list(country_options.keys())
        )
        
        keywords_input = st.text_area(
            "Enter keywords (one per line)",
            "fitness tracker\nworkout\nmeditation"
        )
        
        analyze_button = st.button("Analyze Keywords")

    if analyze_button:
        initial_terms = [k.strip() for k in keywords_input.split("\n") if k.strip()]
        
        if not initial_terms:
            st.error("Please enter at least one keyword")
            return

        scraper = AppStoreKeywordScraper()
        results = scraper.analyze_keywords(initial_terms, country_options[selected_country])
        
        if not results.empty:
            st.subheader("Results")
            st.dataframe(results)
            
            # Download button
            csv = results.to_csv(index=False)
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name=f"app_store_keywords_{country_options[selected_country]}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.error("No data could be collected. Please try different keywords or try again later.")

if __name__ == "__main__":
    main()