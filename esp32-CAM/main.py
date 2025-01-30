from machine import Pin 
from machine import deepsleep
import time,ubinascii,network,camera,esp32,gc
from simple import MQTTClient

#Wi-Fi Credentials
_ssid=""
_pwd=""
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

#Variables
infraredPin=Pin(12,Pin.OUT)
readIFstate=Pin(13,Pin.IN)
mqtt_broker_IP=""
wake=Pin(14,Pin.IN)

#sensor mod:BS412
esp32.wake_on_ext0(pin=wake,level=esp32.WAKEUP_ANY_HIGH)



def connect_to_wifi():
    
    network_list=wlan.scan()
    
    for network in network_list:
        ssid=network[0].decode('utf-8')
        mac=network[1]
        hid=network[5] 
        
        print(f"SSID : {ssid},MAC : {mac},Hidden? : {hid}") 
    
    while True:
        wlan.disconnect()
        print("Device attempting to connect to ",_ssid)
        wlan.connect(_ssid, _pwd)
        timeout=8
        while timeout>0:
            if wlan.isconnected():
                print("\nDevice successfully connected!")
                print("\nDevice IPv4 : ",wlan.ifconfig()[0])
                return
            time.sleep(1)
            print(".",end="")
            timeout-=1
            
        print(f"Couldn't connect to {_ssid}, trying again...")


#mqtt client
client=MQTTClient(
    client_id="ESP32-CAM_client",
    server=mqtt_broker_IP,
    port=1883,
    user="kate",
    password="betjou"
)

def pubToBroker(string):
    client.connect()
    client.publish(b"espCAM32/image", string)
    client.disconnect()



def take_photo():
    try:
        camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
        print("Camera initialize. Ready to take picture")
        img = camera.capture()
        with open("photo.jpg", "wb") as imgFile:
            imgFile.write(img)
            print("Image captured successfully.")
            gc.collect()
            print("Free memory:", gc.mem_free())
        return img
    except Exception as e:
        print("Could not capture image.")
        return None
    finally:
        camera.deinit()

      
print("Waking up, device booting...")
connect_to_wifi()


print("\nDevice taking photo in")
for i in range(5):
    print(5-i)
    time.sleep(1)
    
infraredPin.value(1)
time.sleep(1)
_IFstateBeforePic = readIFstate.value()
print("_IFstateBeforePic =", _IFstateBeforePic)
img_data=take_photo()
_IFstateAfterPic = readIFstate.value()
print("_IFstateAfterPic =", _IFstateAfterPic)
infraredPin.value(0)

if img_data:
    #convert byte array to string 
    encoded_img=ubinascii.b2a_base64(img_data).decode("utf-8")
    pubToBroker(encoded_img)
    print("Published to broker")
else:
    print("Image data empty")


print("Entering deepsleep")
time.sleep(3) #ensuring my motion sensor goes low before
deepsleep()


