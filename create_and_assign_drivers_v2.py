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

# ── Debug: inspect what a real user looks like ────────────────────────────────
existing_users = api.get('User')
print(f"Found {len(existing_users)} existing users.")
if existing_users:
    sample = existing_users[0]
    print("Sample user fields:")
    for k, v in sample.items():
        print(f"  {k}: {repr(v)}")
print()

# ── Get company group ─────────────────────────────────────────────────────────
groups = api.get('Group')
company_group = next(
    (g for g in groups if g.get('id') == 'GroupCompanyId'),
    groups[0]
)
print(f"Using group: {company_group.get('name', company_group['id'])}\n")

# ── 25 Drivers ────────────────────────────────────────────────────────────────
drivers_data = [
    {"first": "James",      "last": "Carter"},
    {"first": "Michael",    "last": "Thompson"},
    {"first": "Sarah",      "last": "Mitchell"},
    {"first": "Robert",     "last": "Anderson"},
    {"first": "Emily",      "last": "Johnson"},
    {"first": "Carlos",     "last": "Ramirez"},
    {"first": "Maria",      "last": "Gonzalez"},
    {"first": "Luis",       "last": "Hernandez"},
    {"first": "Sofia",      "last": "Torres"},
    {"first": "Diego",      "last": "Morales"},
    {"first": "Dmitri",     "last": "Volkov"},
    {"first": "Natasha",    "last": "Petrenko"},
    {"first": "Aleksander", "last": "Nowak"},
    {"first": "Ivana",      "last": "Horvat"},
    {"first": "Pavel",      "last": "Novak"},
    {"first": "Wei",        "last": "Zhang"},
    {"first": "Yuki",       "last": "Tanaka"},
    {"first": "Priya",      "last": "Patel"},
    {"first": "Jin",        "last": "Park"},
    {"first": "Mei",        "last": "Liu"},
    {"first": "Omar",       "last": "AlRashid"},
    {"first": "Fatima",     "last": "Hassan"},
    {"first": "Karim",      "last": "Mansour"},
    {"first": "Layla",      "last": "Nasser"},
    {"first": "Tariq",      "last": "Ibrahim"},
]

existing_emails = {u.get('name', '').lower() for u in existing_users}

# ── Test with ONE minimal user first ──────────────────────────────────────────
print("── Testing minimal user creation ──")
test = drivers_data[0]
test_email = f"{test['first'].lower()}.{test['last'].lower()}@fleetflea.com"

minimal_user = {
    'name': test_email,
    'firstName': test['first'],
    'lastName': test['last'],
    'password': 'FleetFlea2024!',
    'isDriver': True,
    'groups': [{'id': company_group['id']}],
    'securityGroups': [{'id': 'GroupEverythingSecurityId'}],
}

try:
    result = api.add('User', minimal_user)
    print(f"✅ Test user created! ID: {result}")
    test_success = True
except Exception as e:
    print(f"❌ Test failed: {type(e).__name__}: {e}")
    test_success = False

    # Try even more minimal
    print("\nTrying bare minimum user...")
    bare_user = {
        'name': test_email,
        'firstName': test['first'],
        'lastName': test['last'],
        'password': 'FleetFlea2024!',
        'groups': [{'id': company_group['id']}],
    }
    try:
        result = api.add('User', bare_user)
        print(f"✅ Bare minimum user created! ID: {result}")
        test_success = True
        minimal_user = bare_user  # use this template going forward
    except Exception as e2:
        print(f"❌ Bare minimum also failed: {type(e2).__name__}: {e2}")

print()

# ── Create all 25 drivers if test passed ──────────────────────────────────────
created_drivers = []

if test_success:
    # Add the test user to our list
    created_drivers.append({
        'id': result,
        'name': f"{test['first']} {test['last']}",
        'email': test_email
    })
    existing_emails.add(test_email.lower())

    print("Creating remaining 24 drivers...")
    for i, d in enumerate(drivers_data[1:], 2):
        email = f"{d['first'].lower()}.{d['last'].lower()}@fleetflea.com"

        if email.lower() in existing_emails:
            print(f"  ⚠️  Skipping {d['first']} {d['last']} — already exists")
            continue

        try:
            user_obj = dict(minimal_user)  # copy working template
            user_obj['name'] = email
            user_obj['firstName'] = d['first']
            user_obj['lastName'] = d['last']
            if 'isDriver' in minimal_user:
                user_obj['isDriver'] = True

            driver_id = api.add('User', user_obj)
            created_drivers.append({
                'id': driver_id,
                'name': f"{d['first']} {d['last']}",
                'email': email
            })
            print(f"  ✅ {d['first']} {d['last']:15s} ({email})")
            existing_emails.add(email.lower())

        except Exception as e:
            print(f"  ❌ {d['first']} {d['last']}: {e}")

print(f"\n✅ Created {len(created_drivers)} drivers\n")

# ── Assign drivers to vehicles ────────────────────────────────────────────────
if created_drivers:
    devices = api.get('Device')
    random.shuffle(devices)
    print(f"Assigning {len(created_drivers)} drivers across {len(devices)} vehicles...\n")

    now = datetime.now(timezone.utc)
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
    print(f"✅ Drivers created  : {len(created_drivers)}")
    print(f"✅ Assignments done : {assign_success}")
    print(f"❌ Assignments failed: {assign_failed}")
else:
    print("⚠️  No drivers created — skipping assignments.")
    print("Please paste the full error output so we can debug further.")
