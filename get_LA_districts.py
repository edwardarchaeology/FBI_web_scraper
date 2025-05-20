import requests
import json

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
else:
    print(f"Request failed: {response.status_code} - {response.text}")