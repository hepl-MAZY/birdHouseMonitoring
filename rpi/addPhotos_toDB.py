import paho.mqtt.client as mqtt
import base64
import os
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import json


#Config
bucket="nichoir"
org="hepl"
token=""
url="http://localhost:8086"


#Initialize the InfluxDB client
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

#Write API
write_api = client.write_api(write_options=SYNCHRONOUS)


#Normaly the data struct would be as follows : measurement (like a sql table), tags (key-value pairs that are indexed for fast querying), fields (key-value pairs that store actual data values)
photo_metadata = {
    "measurement": "photos", 
    "data": {  
        "device": "ESP32-CAM",
        "location": "Phuket",
        "path": "/home/kate/birdHouse-monitoring/webPage/public/images/esp32CAM_2024-11-09_17-24-14.jpg", #test img
        "timestamp": datetime.now().isoformat()
    }
}

#Create a Point object -- DATA in JSON format to facilitate display on webpage after!!!!!
point = (
    influxdb_client.Point(photo_metadata["measurement"])
    .field("data", json.dumps(photo_metadata["data"]))  #Store everything as a JSON field
)

#Write the Point to the database
write_api.write(bucket=bucket, org=org, record=point)

print("Photo metadata stored successfully!")
