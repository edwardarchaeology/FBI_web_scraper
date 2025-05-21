import asyncio
import aiohttp
import json

import get_state_districts  # Ensure the LA_districts.json file is downloaded

# -----------------------------------
# CONFIGURATION
# -----------------------------------

# Public FBI Crime Data API key
API_KEY = "iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv"

# UCR (Uniform Crime Reporting) arrest crime codes to query
CRIME_CODES = ["11", "30", "60"]  # Example: 11 = Drug Abuse, 30 = Larceny, 60 = Assault

# Date ranges to split requests into chunks (to manage API size limits)
DATE_CHUNKS = [
    ("01-1995", "12-1999"),
    ("01-2000", "12-2004"),
    ("01-2005", "12-2009"),
    ("01-2010", "12-2015")
]

# Limit the number of concurrent requests (helps prevent throttling)
CONCURRENT_REQUESTS = 15
semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

# -----------------------------------
# ASYNC FUNCTION TO FETCH AGENCY DATA
# -----------------------------------

async def fetch_crime_data(session, ori, crime_code, from_date, to_date):
    """
    Makes an asynchronous GET request to the FBI CDE API for a specific
    agency (ORI), crime code, and date range.

    Parameters:
        session: An aiohttp ClientSession object
        ori (str): Originating Agency Identifier
        crime_code (str): FBI UCR crime code
        from_date (str): Start date (MM-YYYY)
        to_date (str): End date (MM-YYYY)

    Returns:
        dict with metadata and data or None if the request fails
    """
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

# -----------------------------------
# MAIN SCRIPT FUNCTION
# -----------------------------------

async def main():
    # Load the local agency file (downloaded previously)
    with open("LA_districts.json", "r") as f:
        data = json.load(f)

    tasks = []

    # Build a list of all fetch tasks across ORIs, crime codes, and date ranges
    async with aiohttp.ClientSession() as session:
        for district, agencies in data.items():
            for agency in agencies:
                ori = agency["ori"]
                for crime_code in CRIME_CODES:
                    for from_date, to_date in DATE_CHUNKS:
                        tasks.append(fetch_crime_data(session, ori, crime_code, from_date, to_date))

        # Run all API requests concurrently
        results = await asyncio.gather(*tasks)

    # Filter out any failed requests (None)
    clean_results = [r for r in results if r is not None]

    # Save the combined results to a JSON file
    with open("crime_results.json", "w") as f:
        json.dump(clean_results, f, indent=2)

    print(f"Fetched {len(clean_results)} valid results")

# -----------------------------------
# ENTRY POINT FOR SCRIPT EXECUTION
# -----------------------------------

"""
For use in Jupyter Notebooks:
-----------------------------------
import nest_asyncio
nest_asyncio.apply()
await main()
-----------------------------------
If you're running this as a script outside Jupyter, use the block below:
"""

if __name__ == "__main__":
    asyncio.run(main())
