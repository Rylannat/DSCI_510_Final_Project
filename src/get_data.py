import requests
import time
import pandas as pd
from typing import List, Dict

API_KEY = "PuhpHetdCkI2FazmRMaJP5lz8Sebxc9EpShCgAqO"
BASE_URL = "https://api.eia.gov/v2/electricity/electric-power-operational-data/data/"

PAGE_SIZE = 5000
REQUEST_DELAY = 0.2

def fetch_all_eia_data(data_fields: List[str], max_pages: int = 200) -> List[Dict]:
    """
    Fetch paginated data from the EIA v2 API for the specified data fields.

    This function handles EIA's pagination mechanism by repeatedly requesting
    additional pages until either:
        (a) all pages have been retrieved, or
        (b) the maximum number of pages (`max_pages`) is reached.

    Parameters
    ----------
    data_fields : list[str]
        A list of EIA data series names (e.g., ["price", "consumption"]).
        These are appended as `data[i]=...` query parameters in the API request.
    
    max_pages : int, optional (default = 200)
        A safety limit on the maximum number of pages to fetch.
        Prevents infinite loops in case the API returns malformed pagination.

    Returns
    -------
    list[dict]
        A list of JSON records aggregated across all pages.
        Each dict corresponds to one record returned by the API.

    Notes
    -----
    - This function assumes that the API endpoint returns a JSON object with:
        * "data": list of records
        * "links": containing pagination URLs (specifically "next")
    - If the API rate-limits, this function may need try/except or backoff logic.
    """

    all_rows = []
    offset = 0
    page = 1

    while True:
        print(f"Fetching page {page} (offset={offset}) ...")

        params = [
            ("api_key", API_KEY),
            ("frequency", "monthly"),
            ("start", "2020-01"),
            ("end", "2025-01"),
            ("facets[location][]", "CA"),
            ("sort[0][column]", "period"),
            ("sort[0][direction]", "desc"),
            ("offset", offset),
            ("length", PAGE_SIZE),
        ]

        for field in data_fields:
            params.append(("data[]", field))

        response = requests.get(BASE_URL, params=params, timeout=30)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break

        data = response.json()

        if "response" not in data or "data" not in data["response"]:
            print("Unexpected JSON format")
            break

        rows = data["response"]["data"]

        if not rows:
            print("All data fetched.")
            break

        all_rows.extend(rows)
        print(f"Retrieved {len(rows)} rows (Total = {len(all_rows)})")

        offset += PAGE_SIZE
        page += 1

        if page > max_pages:
            print("Reached max_pages limit.")
            break

        time.sleep(REQUEST_DELAY)

    return all_rows


data_fields = [
    "ash-content",
    "consumption-for-eg",
    "consumption-for-eg-btu",
    "consumption-uto",
    "consumption-uto-btu",
    "cost",
    "cost-per-btu",
    "generation",
    "heat-content",
    "receipts",
    "receipts-btu",
    "stocks",
    "sulfur-content",
    "total-consumption",
    "total-consumption-btu"
]

print("Starting EIA API download...")
rows = fetch_all_eia_data(data_fields)

df = pd.DataFrame(rows)
df.to_csv("C:/Users/Rylan Lewis/Desktop/USC/DSCI 510/DSCI_510_Final_Project/data/raw/eia_raw_data.csv", index=False)

print("\nData saved")