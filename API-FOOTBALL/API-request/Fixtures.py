import http.client
import json

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': ""
    }

conn.request("GET", "/fixtures?league=4&season=2020", headers=headers)

res = conn.getresponse()
data = res.read()
pretty = json.loads(data)


