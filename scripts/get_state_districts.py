import requests
import json
import pandas as pd

# FBI Crime Data API key (public testing account)
API_KEY = "iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv"
STATE = "LA"

# API endpoint to retrieve law enforcement agencies in Louisiana (by state abbreviation)
url = f"https://api.usa.gov/crime/fbi/cde/agency/byStateAbbr/{STATE}?API_KEY={API_KEY}"


# Make a GET request to the FBI API
response = requests.get(url)

# If the request is successful (status code 200), process the response
if response.status_code == 200:
    # Parse JSON response into a Python dictionary
    data = response.json()

    # Save raw JSON response to file
    with open(f"./data/raw/{STATE}_districts.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved response to {STATE}_districts.json")

    # Flatten the nested JSON into a list of agency records with parish info
    flat_data = []
    for parish, agencies in data.items():
        for agency in agencies:
            agency["parish"] = parish  # Add parish name as a new field
            flat_data.append(agency)

    # Convert the flattened data into a Pandas DataFrame
    df = pd.DataFrame(flat_data)

    # Convert 'nibrs_start_date' strings to datetime objects (if applicable)
    df["nibrs_start_date"] = pd.to_datetime(df["nibrs_start_date"], errors="coerce")

    # Export the cleaned, flat data to a CSV file
    df.to_csv(f"./data/flat/{STATE}_agencies_flat.csv", index=False)
    print(f"Saved flat form of response to {STATE}_agencies_flat.csv")

else:
    # Print error message if the API request fails
    print(f"Request failed: {response.status_code} - {response.text}")