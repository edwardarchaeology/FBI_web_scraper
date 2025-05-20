import requests
import json
import pandas as pd

# API key from FBI API public testing account
API_KEY = "iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv"

url = f"https://api.usa.gov/crime/fbi/cde/agency/byStateAbbr/LA?API_KEY={API_KEY}"

# Make the request
response = requests.get(url)

# Check for success
if response.status_code == 200:
    data = response.json()
    with open("LA_districts.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Saved response to LA_districts.json")
    
    flat_data = []
    for parish, agencies in data.items():
        for agency in agencies:
            agency["parish"] = parish  # add the parish name as a column
            flat_data.append(agency)

    # Convert to DataFrame
    df = pd.DataFrame(flat_data)

    # Optional: convert nibrs_start_date to datetime
    df["nibrs_start_date"] = pd.to_datetime(df["nibrs_start_date"], errors="coerce")
    df.to_csv("LA_agencies_flat.csv", index=False)
    print("Saved flat form of response to LA_agencies_flat.csv")
    

else:
    print(f"Request failed: {response.status_code} - {response.text}")