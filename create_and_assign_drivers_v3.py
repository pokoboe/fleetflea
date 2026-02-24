import mygeotab
import random
from datetime import datetime, timezone

# ── Credentials ────────────────────────────────────────────────────────────────
api = mygeotab.API(
    username='anton.kazakoff@gmail.com',
    password='$8MZMB@$*S8.rzX',
    database='demo_fleetflea',
    server='my.geotab.com'
)
api.authenticate()
print("✅ Connected to Geotab\n")

# ── Inspect an existing user to learn the correct field structure ──────────────
existing_users = api.get('User')
print(f"Found {len(existing_users)} existing users.")
if existing_users:
    sample = existing_users[0]
    print(f"Sample user keys: {list(sample.keys())}\n")

existing_emails = {u.get('name', '').lower() for u in existing_users}

# ── Get company group ──────────────────────────────────────────────────────────
groups = api.get('Group')
company_group = next((g for g in groups if g.get('id') == 'GroupCompanyId'), groups[0])
print(f"Using group: {company_group.get('name', company_group['id'])}\n")

# ── 25 Mixed International Drivers ────────────────────────────────────────────
drivers_data = [
    # American
    {"first": "James",      "last": "Carter"},
    {"first": "Michael",    "last": "Thompson"},
    {"first": "Sarah",      "last": "Mitchell"},
    {"first": "Robert",     "last": "Anderson"},
    {"first": "Emily",      "last": "Johnson"},
    # Hispanic
    {"first": "Carlos",     "last": "Ramirez"},
    {"first": "Maria",      "last": "Gonzalez"},
    {"first": "Luis",       "last": "Hernandez"},
    {"first": "Sofia",      "last": "Torres"},
    {"first": "Diego",      "last": "Morales"},
    # Eastern European
    {"first": "Dmitri",     "last": "Volkov"},
    {"first": "Natasha",    "last": "Petrenko"},
    {"first": "Aleksander", "last": "Nowak"},
    {"first": "Ivana",      "last": "Horvat"},
    {"first": "Pavel",      "last": "Novak"},
    # Asian
    {"first": "Wei",        "last": "Zhang"},
    {"first": "Yuki",       "last": "Tanaka"},
    {"first": "Priya",      "last": "Patel"},
    {"first": "Jin",        "last": "Park"},
    {"first": "Mei",        "last": "Liu"},
    # Middle Eastern
    {"first": "Omar",       "last": "AlRashid"},
    {"first": "Fatima",     "last": "Hassan"},
    {"first": "Karim",      "last": "Mansour"},
    {"first": "Layla",      "last": "Nasser"},
    {"first": "Tariq",      "last": "Ibrahim"},
]

# ── Create Drivers ─────────────────────────────────────────────────────────────
print("Creating 25 drivers...")
created_drivers = []

for i, d in enumerate(drivers_data, 1):
    email = f"{d['first'].lower()}.{d['last'].lower()}@fleetflea.com"

    if email.lower() in existing_emails:
        print(f"  ⚠️  Skip {d['first']} {d['last']} — already exists")
        continue

    try:
        # Minimal clean User object — only fields the API reliably accepts
        user_obj = {
            'name': email,
            'firstName': d['first'],
            'lastName': d['last'],
            'password': 'FleetFlea2024!',
            'isDriver': True,
            'companyGroups': [{'id': company_group['id']}],
            'securityGroups': [{'id': 'GroupEverythingSecurityId'}],
        }

        driver_id = api.add('User', user_obj)
        created_drivers.append({
            'id': driver_id,
            'name': f"{d['first']} {d['last']}",
            'email': email
        })
        print(f"  ✅ [{i:02d}] {d['first']} {d['last']:15s}  →  {email}")
        existing_emails.add(email.lower())

    except Exception as e:
        print(f"  ❌ [{i:02d}] {d['first']} {d['last']}: {e}")

        # Fallback: try without securityGroups
        try:
            user_obj.pop('securityGroups', None)
            driver_id = api.add('User', user_obj)
            created_drivers.append({
                'id': driver_id,
                'name': f"{d['first']} {d['last']}",
                'email': email
            })
            print(f"       ↩️  Retry OK (no securityGroups): {email}")
            existing_emails.add(email.lower())
        except Exception as e2:
            print(f"       ❌ Retry also failed: {e2}")

print(f"\n✅ Created {len(created_drivers)}/25 drivers\n")

# ── Randomly assign drivers to vehicles ───────────────────────────────────────
if not created_drivers:
    print("⚠️  No drivers created — nothing to assign.")
else:
    devices = api.get('Device')
    random.shuffle(devices)
    now = datetime.now(timezone.utc)

    print(f"Assigning {len(created_drivers)} drivers across {len(devices)} vehicles...\n")
    assign_success = 0
    assign_failed = 0

    for i, device in enumerate(devices):
        driver = created_drivers[i % len(created_drivers)]
        try:
            api.add('DriverChange', {
                'driver': {'id': driver['id']},
                'device': {'id': device['id']},
                'dateTime': now.isoformat(),
                'type': 'DriverLogin',
            })
            print(f"  ✅ {device['name']:30s} → {driver['name']}")
            assign_success += 1
        except Exception as e:
            print(f"  ❌ {device['name']:30s} → FAILED: {e}")
            assign_failed += 1

    print(f"\n{'─'*55}")
    print(f"✅ Drivers created   : {len(created_drivers)}/25")
    print(f"✅ Assignments done  : {assign_success}/{len(devices)}")
    print(f"❌ Assignments failed: {assign_failed}")
    print(f"\n🔑 All driver passwords: FleetFlea2024!")
