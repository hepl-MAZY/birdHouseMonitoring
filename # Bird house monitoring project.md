# Bird house monitoring project

# Flashing Firmware

Download .bin file from Micropython Official site


- esptool --port COM7 erase_flash
- esptool --port COM7 --baud 460800 write_flash -z 0x1000 "C:\Users\katee\Downloads\micropython_camera_feeeb5ea3_esp32_idf4_4.bin"

Firmware

GENERIC
"C:\Users\katee\Downloads\ESP32_GENERIC-20231227-v1.22.0.bin"

PSRAM
"C:\Users\katee\Downloads\micropython_camera_feeeb5ea3_esp32_idf4_4.bin"

"C:\Users\katee\Downloads\micropython_cmake_9fef1c0bd_esp32_idf4.x_ble_camera.bin"

Checking flash

esptool verify_flash --diff yes 0x1000 "C:\Users\katee\Downloads\micropython_camera_feeeb5ea3_esp32_idf4_4.bin"


## Overview

## Steps

### Installing necessary packages

- sudo apt-get install mosquitto mosquitto-clients
- sudo apt install python3-paho-mqtt
- InfluxDB (see doc)
- InfluxCLI


### Workflow

- Micropython program running on esp32CAM that will capture image with IR light when motion sensor detected then publish image (base64) to topic "esp32CAM/image" to RPI broker
- Python program that will subscribe to topic "esp32CAM/image" and when payload received, convert to img from base64 then will write data to "nichoir" bucket on influxDB : https://docs.influxdata.com/influxdb/v2/api-guide/client-libraries/python/
- Bashscript will be responsible for running python program on startup of RPI
- Bashscript will be running as a service
- User Interface will be a webpage running with nodejs, displaying images from the influxdb (nichoir bucket") : https://docs.influxdata.com/influxdb/v2/api-guide/client-libraries/nodejs/
