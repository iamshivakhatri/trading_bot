from dotenv import load_dotenv
import requests
import os

headers = {
    'API_KEY' : os.environ.get('API_KEY'),
    'API_SECRET' : os.environ.get('API_SECRET'),
    'BASE_UR' : os.environ.get('BASE_URL'),
}

