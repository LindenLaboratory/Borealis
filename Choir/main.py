#IMPORTS
import network
import urequests as requests
import json
from machine import Pin
import time

#SETUP
led = Pin(2, Pin.OUT)

#FUNCTIONS
def connect():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect('Borealis', 'pico-pico')
  while not wlan.isconnected():
    pass

def get(endpoint):
    response = requests.get(f'http://192.168.4.1{endpoint}')
    return response.text

def send(jsondata=None):
    if jsondata is None:
        with open('data.json', encoding='utf-8') as f:
            data = json.load(f)
            data["log"] = ">:" + data["log"] + ":<"
        jsondata = data
    response = requests.post('http://192.168.4.1/', json=jsondata)

#MAINLOOP
connect()
print("FEEDBACK Mode Activated")
# Start loop here
print(get("/log"))  # Get log
# Code to get data here
send()  # Send data
print("FEEDBACK Sent")
# End loop here
while True:
    led.value(True)  # FEEDBACK FINISHED
