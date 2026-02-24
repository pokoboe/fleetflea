from dotenv import load_dotenv
from mygeotab import API
import os

load_dotenv()

database = os.getenv('GEOTAB_DATABASE')
username = os.getenv('GEOTAB_USERNAME')
password = os.getenv('GEOTAB_PASSWORD')
server = os.getenv('GEOTAB_SERVER')

print(f"Testing connection to {database}...")

api = API(username=username, password=password, database=database, server=server)
api.authenticate()

print("✓ Authentication successful!")
print(f"✓ Connected to: {database}")
print(f"✓ Server: {server}")

# Try fetching vehicle count
devices = api.get('Device')
print(f"✓ Found {len(devices)} vehicles in database")