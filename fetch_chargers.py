"""
Run this script ONCE locally to generate ev-chargers.json
Then commit that file to your repo — the Add-In loads it as a static asset.

Usage:
    pip install requests
    python fetch_chargers.py

Output: ev-chargers.json  (put it next to greenfleet-iq.html in the repo)
"""

import requests, json

KEY = "f15be0f9-2486-4438-8e59-2c460ae291ea"

# Adjust these centers + radius to match where your fleet actually operates.
# Each entry fetches up to 150 stations within `distance` miles.
REGIONS = [
    {"lat": 43.36,  "lng": -79.65,  "distance": 50, "label": "Toronto"},
    {"lat": 41.85, "lng": -87.65,  "distance": 80,  "label": "Chicago"},
    {"lat": 33.45, "lng": -112.07, "distance": 80,  "label": "Phoenix"},
    {"lat": 29.76, "lng": -95.37,  "distance": 80,  "label": "Houston"},
    {"lat": 39.73, "lng": -104.98, "distance": 80,  "label": "Denver"},
    {"lat": 36.17, "lng": -86.78,  "distance": 80,  "label": "Nashville"},
]

all_stations = {}

for region in REGIONS:
    url = (
        f"https://api.openchargemap.io/v3/poi/?output=json"
        f"&key={KEY}"
        f"&latitude={region['lat']}&longitude={region['lng']}"
        f"&distance={region['distance']}&distanceunit=Miles"
        f"&maxresults=150&compact=true&verbose=false"
    )
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        before = len(all_stations)
        for s in data:
            sid = s.get("ID")
            ai  = s.get("AddressInfo", {})
            if sid and ai.get("Latitude") and ai.get("Longitude"):
                all_stations[sid] = {
                    "lat":        ai["Latitude"],
                    "lng":        ai["Longitude"],
                    "name":       ai.get("Title", "EV Charger"),
                    "address":    ai.get("AddressLine1", ""),
                    "connectors": s.get("NumberOfPoints") or "?",
                    "powerKW":    (s.get("Connections") or [{}])[0].get("PowerKW"),
                }
        added = len(all_stations) - before
        print(f"✅ {region['label']}: {len(data)} fetched, {added} new unique")
    except Exception as e:
        print(f"❌ {region['label']}: {e}")

result = list(all_stations.values())
with open("ev-chargers.json", "w") as f:
    json.dump(result, f, separators=(",", ":"))

print(f"\n✅ Saved {len(result)} stations to ev-chargers.json")
print(f"   File size: {len(json.dumps(result)) / 1024:.0f} KB")
print("\nNext steps:")
print("  1. git add ev-chargers.json")
print("  2. git commit -m 'Add EV charger data'")
print("  3. git push")
