# Birdhouse Monitoring Project

## File Structure

### ESP32-CAM
- [`main.py`](esp32-CAM/main.py)  
  - Runs on the ESP32-CAM.
  - Detects motion and captures images.
  - Publishes image data to the MQTT broker for the Raspberry Pi.

### Raspberry Pi
- [`mqtt_influx.py`](rpi/mqtt_influx.py)  
  - Subscribes to the MQTT topic.
  - Receives image data from ESP32-CAM.
  - Stores received images in InfluxDB.

### Web Backend
- [`server.js`](webPage/server.js)  
  - Node.js backend for serving the web interface.
  - Retrieves images from the database.
  - Serves them to the frontend.

## Overview
This project consists of an **ESP32-CAM** that captures images upon motion detection, a **Raspberry Pi** that subscribes to the MQTT topic and stores the images in InfluxDB, and a **Node.js backend** that serves the images via a web interface.

---

📂 **Project Directory:** `BIRDHOUSE_MONITORING`
