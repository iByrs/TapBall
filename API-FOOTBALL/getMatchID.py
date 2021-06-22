import json
import csv

with open("../Logstash/data/fixtures.json") as file:
    data = json.load(file)

file2 = open("../Dataset/id_match2020.csv", "w")
write = csv.writer(file2)

data = data['response']

for i in range(298):
    array = []
    array.append(data[i]['fixture']['id'])
    array.append(data[i]['goals']['home'])
    array.append(data[i]['goals']['away'])
    write.writerow(array)

print(array)

file.close()
file2.close()