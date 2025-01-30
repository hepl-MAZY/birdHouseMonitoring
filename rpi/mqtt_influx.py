import paho.mqtt.client as mqtt
import base64
import os
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import json

mqttBroker="localhost"
mqttPort=1883
mqttTopic="espCAM32/image"
mqttUsername=""
mqttPassword=""

bucket="nichoir"
org="hepl"
token=""
url="http://localhost:8086"



def on_message(client, userdata, message):
	try:
		#Converting back to raw from base64
		imageData=base64.b64decode(message.payload)
		imageDirectory="/home/kate/birdHouse-monitoring/webPage/public/images/"
		
		os.makedirs(imageDirectory, exist_ok=True)
		
		#Saving image locally 
		timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		imageFilename=f"esp32CAM_{timestamp}.jpg"
		
		imagePath=os.path.join(imageDirectory, imageFilename)
		
		with open(imagePath, "wb") as img_file:
			img_file.write(imageData)
		
  
		#Saving to DB
		client = influxdb_client.InfluxDBClient(
			url=url,
			token=token,
			org=org
		)
		
		#Image metadata
		photo_metadata = {
    "measurement": "photos", 
    "data": {  
        "device": "ESP32-CAM",
        "location": "Phuket",
        "path": imagePath,
        "timestamp": datetime.now().isoformat()
    }
}
  
		write_api = client.write_api(write_options=SYNCHRONOUS)

		# Create a Point object
		point = (
    influxdb_client.Point(photo_metadata["measurement"])
    .field("data", json.dumps(photo_metadata["data"]))  # Store everything as a JSON field
)

		# Write the Point to the database
		write_api.write(bucket=bucket, org=org, record=point)
		
		
		print(f"Successfully saved to {imagePath} and added to DB!")
  
	except Exception as e:
		print(f"Error : {e}")


#Connect to MQTT and sub to topic
mqtt_client=mqtt.Client()
mqtt_client.username_pw_set(mqttUsername,mqttPassword)
mqtt_client.on_message=on_message
mqtt_client.connect(mqttBroker,mqttPort)
print(f"Subscribing to {mqttTopic}")
mqtt_client.subscribe(mqttTopic)

mqtt_client.loop_forever()
