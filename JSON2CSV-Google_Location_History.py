#!/usr/bin/python3
import re
import json
import csv
import pathlib

JSON_data="Records.json"

with open(JSON_data) as f:
    data = json.load(f)

for x in range(len(data["locations"])):
    timestamp_pre=str(data['locations'][x]['timestamp'])
    timestamp=timestamp_pre.split("T")
    date=re.sub(r'-', '/', timestamp[0])
    dateforfilename=re.sub(r'-', '_', timestamp[0])
    time=re.sub(r'Z', '', re.sub(r'\..*', '',timestamp[1]))
    lat=int(data['locations'][x]['latitudeE7'])/1e7
    lon=int(data['locations'][x]['longitudeE7'])/1e7
    CSV_file="Records_" + dateforfilename + ".csv"
    file = pathlib.Path(CSV_file)
    if file.exists ():
        csv_f=open(CSV_file, 'a')
        csv_f.write(str(lat) + "," + str(lon) + "," + str(date) + "," + str(time) +'\n')
    else:
        csv_f=open(CSV_file, 'a')
        csv_f.write('lat,lon,date,time\n')
        csv_f.write(str(lat) + "," + str(lon) + "," + str(date) + "," + str(time) +'\n')
    csv_f.close
print('Done')    

print('for i in *.csv; do gpsbabel -i unicsv -t -f $i -o gpx -F $i.gpx; done')

