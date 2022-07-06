#!/usr/bin/python3
import re
import json
import csv
import pathlib
import subprocess

JSON_data="Records.json"

cmd_pre = subprocess.Popen("rm -rf csv/; rm -rf gpx/; mkdir csv gpx", stdout=subprocess.PIPE, shell=True)

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
    try:
        alt=int(data['locations'][x]['altitude'])
    except:
        alt=1
    CSV_file="csv/Records_" + dateforfilename + ".csv"
    file = pathlib.Path(CSV_file)
    if file.exists ():
        csv_f=open(CSV_file, 'a')
        csv_f.write(str(lat) + "," + str(lon) + "," + str(alt) + "," + str(date) + "," + str(time) +'\n')
    else:
        csv_f=open(CSV_file, 'a')
        csv_f.write('lat,lon,alt,date,time\n')
        csv_f.write(str(lat) + "," + str(lon) + "," + str(alt) + "," + str(date) + "," + str(time) +'\n')
    csv_f.close


cmd_babel = subprocess.Popen("cd csv; for i in *.csv; do trackname=$(echo $i | sed 's/.csv//g' | awk -F'_' '{print $3\"_\"$4}'); gpsbabel -i unicsv -t -f $i -o gpx -x track,title=${trackname} -F ../gpx/$i.gpx; done; cd ..", stdout=subprocess.PIPE, shell=True)
print('Done')    

