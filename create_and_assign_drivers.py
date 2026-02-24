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

# ── 25 Realistic Mixed International Drivers ───────────────────────────────────
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
    {"first": "Omar",       "last": "Al-Rashid"},
    {"first": "Fatima",     "last": "Hassan"},
    {"first": "Karim",      "last": "Mansour"},
    {"first": "Layla",      "last": "Nasser"},
    {"first": "Tariq",      "last": "Ibrahim"},
]

# ── Fetch existing users to avoid duplicate emails ─────────────────────────────
existing_users = api.get('User')
existing_emails = {u.get('name', '').lower() for u in existing_users}
print(f"Found {len(existing_users)} existing users in database.\n")

# ── Get the company root group (required for new users) ───────────────────────
groups = api.get('Group')
company_group = next((g for g in groups if g.get('name') == 'Company Group' or g.get('id') == 'GroupCompanyId'), None)
if not company_group:
    company_group = groups[0]  # fallback to first group
print(f"Using group: {company_group.get('name', company_group['id'])}\n")

# ── Create Drivers ─────────────────────────────────────────────────────────────
print("Creating drivers...")
created_drivers = []
skipped = 0

for i, d in enumerate(drivers_data, 1):
    email = f"{d['first'].lower()}.{d['last'].lower().replace('-', '').replace(' ', '')}@fleetflea.com"

    if email.lower() in existing_emails:
        print(f"  ⚠️  Skipping {d['first']} {d['last']} — email already exists")
        skipped += 1
        continue

    try:
        new_user = {
            'name': email,
            'firstName': d['first'],
            'lastName': d['last'],
            'isDriver': True,
            'employeeNo': f"EMP{i:03d}",
            'password': 'FleetFlea2024!',
            'changePasswordRequired': False,
            'groups': [{'id': company_group['id']}],
            'securityGroups': [{'id': 'GroupEverythingSecurityId'}],
            'userAuthenticationType': 'BasicAuthentication',
        }

        driver_id = api.add('User', new_user)
        created_drivers.append({
            'id': driver_id,
            'name': f"{d['first']} {d['last']}",
            'email': email
        })
        print(f"  ✅ Created: {d['first']} {d['last']:15s} ({email})")

    except Exception as e:
        print(f"  ❌ Failed to create {d['first']} {d['last']}: {e}")

print(f"\n✅ Created {len(created_drivers)} drivers | ⚠️  Skipped {skipped}\n")

# ── Fetch all devices ──────────────────────────────────────────────────────────
devices = api.get('Device')
random.shuffle(devices)
print(f"Found {len(devices)} vehicles. Assigning drivers randomly...\n")

# ── Assign drivers to trucks (random, each driver gets ~2 trucks) ──────────────
print("Assigning drivers to vehicles...")
assign_success = 0
assign_failed = 0

if not created_drivers:
    print("⚠️  No drivers were created — nothing to assign.")
else:
    now = datetime.now(timezone.utc)

    for i, device in enumerate(devices):
        # Cycle through drivers randomly (each gets ~2 trucks)
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

# ── Summary ────────────────────────────────────────────────────────────────────
print(f"\n{'─'*55}")
print(f"✅ Drivers created : {len(created_drivers)}")
print(f"✅ Assignments done: {assign_success}")
print(f"❌ Assignments failed: {assign_failed}")
print(f"\nAll drivers can log in with password: FleetFlea2024!")
print("Recommend changing passwords after first login.")
