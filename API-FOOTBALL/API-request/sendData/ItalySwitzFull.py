import csv
import time
import json

def getMatchStatistics(json_f, f):
    writer = csv.writer(f)
    try:
        row = [json_f['response'][0]['team']['name']]
        row2 = [json_f['response'][1]['team']['name']]
        for i in range(16):
            if i != 3 and i!=4 and i!=5 and i!=8 and i!=12:
                value = json_f['response'][0]['statistics'][i]['value']
                value2 = json_f['response'][1]['statistics'][i]['value']
                if value!=None:
                    if str(value).find('%'):
                        value = str(value).replace('%','')
                    row.append(value)
                else:
                    row.append(0)
                if value2!=None:
                    if str(value2).find('%'):
                        value = str(value2).replace('%','')
                    row2.append(value)
                else:
                    row2.append(0)
        writer.writerow(row)
        writer.writerow(row2)  
    except:
        print('errore')
        pass

for i in range(20):
    path = "../../../Dataset/Simulation/ItalySwizt2020/Italy_swiss%d.json" % (i+1)
    file = "../../../Dataset/data.csv"
    with open(path, "r") as match, open(file, "a") as f:
        json_f = json.load(match)
        getMatchStatistics(json_f, f)
        match.close()
        time.sleep(10)
    match.close()
    f.close()        


    #"../../../Dataset/Simulation/CzechEngland2020/CzechEnglash%d.json" 