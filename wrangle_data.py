import json
import pandas as pd

import fbi_api_calls  # Ensures API calls are available if needed before flattening

# -----------------------------------
# LOAD CRIME RESULTS FROM JSON
# -----------------------------------

# Load the JSON output from previous FBI API requests
with open("crime_results.json", "r") as f:
    data = json.load(f)

rows = []

# -----------------------------------
# FLATTEN NESTED JSON INTO ROWS
# -----------------------------------

for entry in data:
    ori = entry.get("ori")  # Agency identifier
    crime_code = entry.get("crime_code")  # UCR crime code
    from_date = entry.get("from")  # Start date of time range
    to_date = entry.get("to")      # End date of time range
    data_block = entry.get("data", {})  # Contains all nested data sections

    # Extract nested blocks (safely handle missing keys)
    rates = data_block.get("rates", {})
    actuals = data_block.get("actuals", {})
    tooltips = data_block.get("tooltips", {}).get("Percent of Population Coverage", {})
    populations = data_block.get("populations", {}).get("population", {})
    participated = data_block.get("populations", {}).get("participated_population", {})

    # Iterate through each source in the rates block (e.g., "Louisiana Arrests")
    for source, rate_series in rates.items():
        source_base = source.replace(" Arrests", "")  # Normalize name for lookup in other blocks

        for date, rate in rate_series.items():
            # Safely gather aligned data across all blocks
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

# -----------------------------------
# CONVERT TO DATAFRAME
# -----------------------------------

# Convert all rows to a Pandas DataFrame
df = pd.DataFrame(rows)

# Convert "MM-YYYY" string dates to datetime objects
df["date"] = pd.to_datetime(df["date"], format="%m-%Y", errors="coerce")

# -----------------------------------
# EXPORT FLATTENED DATA
# -----------------------------------

# Print sample of resulting flat DataFrame
print(df.head())

# Export to CSV
df.to_csv("flattened_crime_data.csv", index=False)
