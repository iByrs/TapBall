import http.client
import json
file = open("../Logstash/data/euro_teams.json", "w")

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "8bfd50903a0ad9fa6812f79fcfb24fd0"
    }

conn.request("GET", "/teams?league=4&season=2020", headers=headers)

res = conn.getresponse()
data = res.read()
pretty = json.loads(data)
#print(data.decode("utf-8"))
file.write(json.dumps(pretty, indent=4, sort_keys=True))
file.close()
