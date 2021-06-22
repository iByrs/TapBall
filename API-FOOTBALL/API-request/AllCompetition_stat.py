import http.client
import json

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': ""
    }

conn.request("GET", "/teams/statistics?season=2016&team=768&league=4", headers=headers)

res = conn.getresponse()
data = res.read()
pretty = json.loads(data)


