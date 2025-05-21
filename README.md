# Louisiana FBI Crime Data Extractor

This repository contains a set of Python scripts for extracting, flattening, and exporting arrest data from the FBI Crime Data Explorer (CDE) API for law enforcement agencies in Louisiana.

## 📦 Project Structure

- `get_LA_districts.py`:  
  Fetches a list of Louisiana law enforcement agencies and their metadata from the FBI API. Outputs:
  - `LA_districts.json` (raw API response)
  - `LA_agencies_flat.csv` (flattened metadata)

- `fbi_api_calls.py`:  
  Asynchronously requests monthly arrest data for selected Uniform Crime Reporting (UCR) crime codes using the FBI API. Outputs:
  - `crime_results.json` (nested data per agency/crime/date chunk)

- `flatten_results.py`:  
  Converts the nested structure in `crime_results.json` to a flat CSV file combining:
  - Arrest rates
  - Actual arrest counts (where available)
  - Population and participation stats
  - Coverage percentages  
  Output: `flattened_crime_data.csv`

## 📊 Example Fields in Flattened Output

| ori       | crime_code | source                      | date     | rate | actual | population | coverage_pct |
|-----------|------------|-----------------------------|----------|------|--------|------------|----------------|
| LA0640100 | 11         | Winnfield Police Department | 2000-01  | 0.78 | 0      | 5749       | 92.57          |

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/louisiana-fbi-crime-data.git
cd louisiana-fbi-crime-data
```

### 2. Set up the environment

```bash
pip install -r requirements.txt
```

**Required packages:**
- `aiohttp`
- `asyncio`
- `pandas`
- `requests`
- `nest_asyncio` (for running in Jupyter)

### 3. Run the scripts in order

```bash
python get_LA_districts.py
python fbi_api_calls.py
python flatten_results.py
```

> Note: `fbi_api_calls.py` uses asynchronous batch requests to avoid rate limits.

## 🧠 Notes

- Uses the [FBI Crime Data Explorer API](https://crime-data-explorer.fr.cloud.gov/api)
- Currently limited to crime codes `11` (homicide), `30` (robbery), and `60` (assault)
- Time ranges split into chunks for efficient API querying
- Designed for reproducibility and ease of adaptation to other states or codes

## 📁 Output Files

| File                    | Description                              |
|-------------------------|------------------------------------------|
| `LA_districts.json`     | Raw list of LA agencies by parish        |
| `LA_agencies_flat.csv` | Flat metadata with one row per agency    |
| `crime_results.json`    | Raw nested arrest data from FBI          |
| `flattened_crime_data.csv` | Cleaned, analysis-ready data           |

## 📜 License

MIT License. See `LICENSE` file.

## 🤝 Acknowledgments

Thanks to the FBI Crime Data Explorer team and the U.S. government for providing public access to criminal justice datasets.