import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
BASE_URL = os.environ.get("BASE_URL")

print(API_KEY)
print(API_SECRET)
print(BASE_URL)
print(os.environ.get("key"))