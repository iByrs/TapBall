import http.client
import json

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "8bfd50903a0ad9fa6812f79fcfb24fd0"
    }
# INSERT ID OF THE MATCH AFTER 'FIXTURE='
conn.request("GET", "/fixtures/statistics?fixture=", headers=headers)

res = conn.getresponse()
data = res.read()
pretty = json.loads(data)


