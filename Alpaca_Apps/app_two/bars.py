from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

url = "https://data.alpaca.markets/v2/stocks/bars"

params = {
    "symbols": "TSLA",
    "timeframe": "1Min",
    "start": "2023-07-01",
    "end": "2023-07-31",
    "limit": 1000,
    "adjustment": "raw",
    "feed": "sip",
    "sort": "asc"
}

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": os.environ.get("API_KEY"),
    "APCA-API-SECRET-KEY": os.environ.get("API_SECRET")
}

response = requests.get(url, headers=headers, params=params)

print(json.dumps(response.json(), indent=4))

with open("data.txt", "w") as f:
    f.write(json.dumps(response.json(), indent=4))
    