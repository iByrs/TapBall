import http.client
import time
import json

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "8bfd50903a0ad9fa6812f79fcfb24fd0"
    }
# INSERT ID OF THE MATCH AFTER 'FIXTURE='
for i in range(100):
    path = "../Dataset/CzechEngland/CzechEnglash%d.json" %i
    with open(path, 'w') as file:
        conn.request("GET", "/fixtures/statistics?fixture=657705", headers=headers)
        res = conn.getresponse()
        data = res.read()
        pretty = json.loads(data)
        file.write(pretty)
        file.close()
        time(250)
# ID = 657705