
import json
import pandas as pd

import fbi_api_calls

with open("crime_results.json", "r") as f:
    data = json.load(f)
rows = []

for entry in data:
    ori = entry.get("ori")
    crime_code = entry.get("crime_code")
    from_date = entry.get("from")
    to_date = entry.get("to")
    data_block = entry.get("data", {})

    rates = data_block.get("rates", {})
    actuals = data_block.get("actuals", {})
    tooltips = data_block.get("tooltips", {}).get("Percent of Population Coverage", {})
    populations = data_block.get("populations", {}).get("population", {})
    participated = data_block.get("populations", {}).get("participated_population", {})

    for source, rate_series in rates.items():
        source_base = source.replace(" Arrests", "")

        for date, rate in rate_series.items():
            row = {
                "ori": ori,
                "crime_code": crime_code,
                "from": from_date,
                "to": to_date,
                "source": source_base,
                "date": date,
                "rate": rate,
                "actual": actuals.get(source, {}).get(date),
                "population": populations.get(source_base, {}).get(date),
                "participated_population": participated.get(source_base, {}).get(date),
                "coverage_pct": (tooltips.get(source_base) or {}).get(date)
            }
            rows.append(row)

# Convert to DataFrame
df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"], format="%m-%Y", errors="coerce")

# Optional: Preview or export
print(df.head())
df.to_csv("flattened_crime_data.csv", index=False)