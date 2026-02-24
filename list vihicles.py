import mygeotab

api = mygeotab.API(
    username='anton.kazakoff@gmail.com',
    password='$8MZMB@$*S8.rzX',
    database='demo_fleetflea',
    server='my.geotab.com'
)
api.authenticate()

devices = api.get('Device')
for i, d in enumerate(devices, 1):
    print(f'{i}. {d["name"]} | ID: {d["id"]}')

print(f'\nTotal: {len(devices)} vehicles')