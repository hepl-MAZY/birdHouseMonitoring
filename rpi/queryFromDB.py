import paho.mqtt.client as mqtt
import base64
import os
from datetime import datetime
import influxdb_client
import json
from influxdb_client.client.write_api import SYNCHRONOUS

#Config
bucket="nichoir"
org="hepl"
token=""
url="http://localhost:8086"

#Initialize the InfluxDB client
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

#Query to fetch photo metadata
query = f'''
from(bucket: "{bucket}")
  |> range(start: -1d)  // Adjust the time range as needed
  |> limit(n: 10)       // Limit to avoid overload
'''

result = client.query_api().query(query=query)

#Print all raw records
for table in result:
    for record in table.records:
        print(record.values)