# App Store Keyword Analysis Tool 🔍

A streamlit-based tool to analyze App Store keywords, search volumes, and competitive metrics across different countries.

## Features ✨

- Search keyword suggestions from App Store
- Analyze app data for specific keywords
- Cross-country analysis support
- Export results to CSV
- Visualization of key metrics
- Real-time data processing

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/yourusername/app-store-keyword-analysis.git
cd app-store-keyword-analysis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage 💻

1. Run the Streamlit app:
```bash
streamlit run app_store.py
```

2. In the web interface:
   - Select target country
   - Enter keywords (one per line)
   - Click "Analyze Keywords"
   - View results and download CSV

## Dependencies 📚

- streamlit
- pandas
- requests
- plotly

## Example Keywords 📝

Some popular categories to analyze:
- Productivity: "task manager", "to do list"
- Health: "fitness tracker", "meditation app"
- Social: "messaging app", "photo sharing"
- Finance: "budget tracker", "investing app"

## Contributing 🤝

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License 📄

[MIT](https://choosealicense.com/licenses/mit/)

---

También deberíamos crear un archivo `requirements.txt`:

```text
streamlit>=1.10.0
pandas>=1.3.0
requests>=2.26.0
plotly>=5.3.0
```

¿Quieres que añada alguna sección adicional al README o que detalle más alguna parte?
