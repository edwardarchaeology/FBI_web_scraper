import asyncio
import aiohttp
import json

import get_LA_districts
# %%
API_KEY = "iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv"
CRIME_CODES = ["11", "30", "60"]
DATE_CHUNKS = [
    ("01-1995", "12-1999"),
    ("01-2000", "12-2004"),
    ("01-2005", "12-2009"),
    ("01-2010", "12-2015")
]
# %%
CONCURRENT_REQUESTS = 15
semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

async def fetch_crime_data(session, ori, crime_code, from_date, to_date):
    url = (
        f"https://api.usa.gov/crime/fbi/cde/arrest/agency/"
        f"{ori}/{crime_code}?type=counts&from={from_date}&to={to_date}&API_KEY={API_KEY}"
    )
    async with semaphore:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return {
                        "ori": ori,
                        "crime_code": crime_code,
                        "from": from_date,
                        "to": to_date,
                        "data": await response.json()
                    }
                else:
                    print(f"Failed for {ori} - {crime_code} ({from_date}–{to_date}): {response.status}")
                    return None
        except Exception as e:
            print(f"Error fetching {ori} - {crime_code} ({from_date}–{to_date}): {e}")
            return None

async def main():
    # Load JSON file
    with open("LA_districts.json", "r") as f:
        data = json.load(f)

    tasks = []

    async with aiohttp.ClientSession() as session:
        for district, agencies in data.items():  # Limit to first 2 districts for testing
            for agency in agencies:
                ori = agency["ori"]
                for crime_code in CRIME_CODES:
                    for from_date, to_date in DATE_CHUNKS:
                        tasks.append(fetch_crime_data(session, ori, crime_code, from_date, to_date))

        results = await asyncio.gather(*tasks)

    # Optional: remove None values
    clean_results = [r for r in results if r is not None]

    # Save to file
    with open("crime_results.json", "w") as f:
        json.dump(clean_results, f, indent=2)

    print(f"Fetched {len(clean_results)} valid results")

""" For working in jupyter notebooks, uncomment the following lines:
import nest_asyncio
nest_asyncio.apply()
await main() 

and comment out the if __name__ == "__main__": block below."
"""
if __name__ == "__main__":
    asyncio.run(main())