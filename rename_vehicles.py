import mygeotab

# ── Credentials ────────────────────────────────────────────────────────────────
api = mygeotab.API(
    username='anton.kazakoff@gmail.com',
    password='$8MZMB@$*S8.rzX',
    database='demo_fleetflea',
    server='my.geotab.com'
)
api.authenticate()
print("✅ Connected to Geotab\n")

# ── New names for 50 trucks ────────────────────────────────────────────────────
new_names = [
    "Ford F-150 #01",        "Ford F-150 #02",        "Ford F-250 #03",
    "Ford F-250 #04",        "Ford F-350 #05",        "Ford F-350 #06",
    "Ford Ranger #07",       "Ford Ranger #08",       "Ford Maverick #09",
    "Ford F-450 #10",
    "Chevy Silverado 1500 #11", "Chevy Silverado 1500 #12", "Chevy Silverado 2500 #13",
    "Chevy Silverado 2500 #14", "Chevy Silverado 3500 #15", "Chevy Colorado #16",
    "Chevy Colorado #17",    "Chevy Colorado #18",    "Chevy Silverado 1500 #19",
    "Chevy Silverado 3500 #20",
    "RAM 1500 #21",          "RAM 1500 #22",          "RAM 2500 #23",
    "RAM 2500 #24",          "RAM 3500 #25",          "RAM 3500 #26",
    "RAM 1500 TRX #27",      "RAM 2500 Power Wagon #28", "RAM 1500 #29",
    "RAM 3500 #30",
    "GMC Sierra 1500 #31",   "GMC Sierra 1500 #32",   "GMC Sierra 2500 #33",
    "GMC Sierra 2500 #34",   "GMC Sierra 3500 #35",   "GMC Canyon #36",
    "GMC Canyon #37",        "GMC Sierra 1500 #38",   "GMC Sierra 3500 #39",
    "GMC Canyon #40",
    "Toyota Tacoma #41",     "Toyota Tacoma #42",     "Toyota Tundra #43",
    "Toyota Tundra #44",     "Toyota Tacoma #45",     "Toyota Tundra #46",
    "Toyota Tacoma #47",     "Toyota Tundra #48",     "Toyota Tacoma #49",
    "Toyota Tundra #50",
]

# ── Fetch current devices ──────────────────────────────────────────────────────
devices = api.get('Device')
devices_sorted = sorted(devices, key=lambda d: d['id'])
print(f"Found {len(devices_sorted)} vehicles. Renaming...\n")

# ── Rename each device ────────────────────────────────────────────────────────
success, failed = 0, 0

for i, device in enumerate(devices_sorted):
    old_name = device['name']
    new_name = new_names[i] if i < len(new_names) else f"Truck #{i+1:02d}"

    try:
        device['name'] = new_name
        api.set('Device', device)
        print(f"  ✅ {old_name:20s} → {new_name}")
        success += 1
    except Exception as e:
        print(f"  ❌ {old_name:20s} → FAILED: {e}")
        failed += 1

# ── Summary ───────────────────────────────────────────────────────────────────
print(f"\n{'─'*50}")
print(f"✅ Renamed: {success}  |  ❌ Failed: {failed}")
