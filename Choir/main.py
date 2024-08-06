#IMPORTS
import io
from machine import Pin, PWM
import utime
from PicoOLED1point3spi import OLED_1inch3
import micropython
import network
import urequests as requests
import json
import machine

#SETUP
b0 = Pin(15, Pin.IN, Pin.PULL_UP)
b1 = Pin(17, Pin.IN, Pin.PULL_UP)
error = "404"
username = ""
money = 0.00
line = 1
bindex = -1
stats = None

#FUNCTIONS
    #ABSTRACTION FUNCTIONS
def truncation(txt):
    if len(txt) > 16:
        txt = txt[:13] + "..."
    return txt
def split_text(text):
    initial_chunks = text.split('\n')
    final_chunks = []
    for chunk in initial_chunks:
        while len(chunk) > 16:
            if len(final_chunks) == 3:
                final_chunks.append(truncation(chunk[:16]))
                return final_chunks
            final_chunks.append(chunk[:16])
            chunk = chunk[16:]
        final_chunks.append(chunk)
        if len(final_chunks) == 4:
            break
    if len(final_chunks) > 4:
        final_chunks = final_chunks[:3]
        final_chunks.append(truncation(final_chunks.pop()))
    return final_chunks
    #DISPLAY FUNCTIONS
def display_clear_all(display):
    display.fill(0x0000)
def display_clear_line1(display):
    display.fill_rect(0, 0, 128, 16, display.black)
def display_clear_line2(display):
    display.fill_rect(0, 16, 128, 16, display.black)
def display_clear_line3(display):
    display.fill_rect(0, 32, 128, 16, display.black)
def display_clear_line4(display):
    display.fill_rect(0, 48, 128, 16, display.black)
def display_line1(display, txt):
    txt = truncation(txt)
    display_clear_line1(display)
    display.text(txt, 0, 4, display.white)
def display_line2(display, txt):
    txt = truncation(txt)
    display_clear_line2(display)
    display.text(txt, 0, 20, display.white)
def display_line3(display, txt):
    txt = truncation(txt)
    display_clear_line3(display)
    display.text(txt, 0, 36, display.white)
def display_line4(display, txt):
    txt = truncation(txt)
    display_clear_line4(display)
    display.text(txt, 0, 52, display.white)
def display_splash(display,a,b):
    display_clear_all(display)
    display.rect(0, 0, 128, 64, display.white)
    spacea = round(((16-len(a))/2))*" "
    spaceb = round(((16-len(b))/2))*" "
    a = spacea + a + spacea
    b = spaceb + b + spaceb
    display.text(a, 0, 22, display.white)
    display.text(b, 0, 40, display.white)
    utime.sleep(0.1)
    display.show()
    utime.sleep(2.5)
    display_clear_all(display)
    display.show()
    utime.sleep(0.1)
def display_splash_perm(display,a,b):
    display_clear_all(display)
    display.rect(0, 0, 128, 64, display.white)
    spacea = round(((16-len(a))/2))*" "
    spaceb = round(((16-len(b))/2))*" "
    a = spacea + a + spacea
    b = spaceb + b + spaceb
    display.text(a, 0, 22, display.white)
    display.text(b, 0, 40, display.white)
    display.show()
def display_disconnected(display,line):
    global error
    if line != None:
        if line == 1:
            display_clear_all(display)
        eval(f'display_line{str(line)}(display, "Failed")')
        display.show()
        utime.sleep(1)
    display_clear_all(display)
    display.rect(0, 0, 128, 64, display.white)
    display.text("  Disconnected  ", 0, 22, display.white)
    display.text(f"      e{error}      ", 0, 40, display.white)
    utime.sleep(0.1)
    display.show()
    while b0.value() == 1 and b1.value() == 1:
        utime.sleep(0.1)
    if b0.value() == 0 and b1.value() == 0:
        machine.reset()
def display_text(display,txt):
    display_clear_all(display)
    chunks = split_text(txt)
    try:
        display_line1(display,chunks[0])
        display_line2(display,chunks[1])
        display_line3(display,chunks[2])
        display_line4(display,chunks[3])
    except:
        pass
    display.show()

    #NETWORK FUNCTIONS
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('Borealis', 'pico-pico')
    for _ in range(5):
        utime.sleep(1)
        if wlan.isconnected():
            return True
    return False
def getaccount():
    with open("account.txt","r") as f:
        username = f.readline().replace("\n","")
    if username == "":
        return None
    else:
        return username
def get(endpoint):
    response = requests.get(f'http://192.168.4.1{endpoint}')
    return response.text
def send(jsondata=None):
    request_header={
        'X-HTTP-Method-Override': 'GET'
    }
    if jsondata is None:
        with open('data.json', encoding='utf-8') as f:
            data = json.load(f)
            data["log"] = data["log"]
        jsondata = data
    response = requests.post('http://192.168.4.1/', json=jsondata,headers=request_header)
    return response.text
def execute(code,display):
    codeplus = """
def GET(endpoint):
    return get(endpoint)
def SEND(jsondata):
    return send(jsondata)
def DISPLAY(text):
    print(text)
    display_text(display,text)
    utime.sleep(0.25)
def B0():
    return b0.value()
def B1():
    return b1.value()
def B2():
    if b1.value() == 0 and b0.value() == 0:
        return 0
    else:
        return 1
def ACCOUNT():
    return getaccount()
"""+"\n"+code.replace("\t","  ")
    print(codeplus)
    display_clear_all(display)
    display.show()
    exec(codeplus)

#MAINLOOP
    #SETUP
print("FEEDBACK Mode Activated")
display = OLED_1inch3()
    #MAINLOOP
def mainloop(apps,display):
    global b0,b1,bindex,line
    display_clear_all(display)
    display_text(display,"Syncing with network...")
    display.show()
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    connect()
    while True:
        display_splash(display,"App Store","v0.0.1")
        if apps == None:
            display_clear_all(display)
            display_line1(display,"Getting Apps...")
            display.show()
            apps = [app.replace(":.","\n").replace("\r","") for app in get("/app/list").split("\n")]
            apps.remove("")
        display_splash_perm(display,"App Store",str(len(apps))+" Apps")
        line = None
        error = "500"
        while True:
            if b0.value() == 0 and b1.value() == 0:
                break
            elif b1.value() == 0:
                if bindex < len(apps)-1:
                    bindex += 1
                else:
                    bindex = 0
                print(bindex)
                display_text(display,apps[bindex])
                utime.sleep(0.15)
            elif b0.value() == 0:
                if bindex >= 0:
                    name = apps[bindex].split("\n")[0].split("Name: ")[1].strip().lower()
                    execute(get(f"/app/{name}.py"),display)
                    apps = None
                    break
            else:
                utime.sleep(0.1)
    #CONNECTION
while True:
    display_clear_all(display)
    try:
        display_line1(display, "Connecting...")
        display.show()
        print("Connecting...")
        if connect() == False:
            print("Disconnected")
            display_disconnected(display,line)
            continue
        print("Connected")
        display_line1(display, "Connected")
        display.show()
        error,line = "503",2
        username = getaccount()
        if username == None:
            print("Getting Account")
            display_line2(display, "Getting Account...")
            display.show()
            logged = get("/log").split("\n")[-10:]
            print(logged)
            for i in logged:
                if "Account '" in i and "' Created" in i:
                    username = i.split("'")[1]
            if username == None:
                print("Failed")
                error = "404"
                display_disconnected(display,line)
                continue
            else:
                with open("account.txt","w") as f:
                    f.write(username)
            print(f"Account Synced (username: {username})")
            display_line2(display, "Account Synced")
            display.show()
        else:
            print("Getting Apps")
            display_line2(display, "Getting Apps...")
            display.show()
            apps = [app.replace(":.","\n").replace("\r","") for app in get("/app/list").split("\n")]
            apps.remove("")
            display_line2(display, "Apps Fetched")
            display.show()
            print(apps)
        line,error = 3,"503"
        print("Fetching Stats")
        display_line3(display, "Getting Stats...")
        display.show()
        money = get(f"/account?v=0&u={username}").split("\n\n")[0]
        if "Error 400" in money:
            print("Failed")
            error = "400"
            display_disconnected(display,line)
        display_line3(display, "Stats Fetched")
        display.show()
        display_line4(display, "Booting...")
        display.show()
        utime.sleep(1)
        line = 1
        display_splash(display,"Borealis","v1.2.1")
        display_splash(display,username,money)
        mainloop(apps,display)
        continue
    except Exception as e:
        print(e)
        display_disconnected(display,line)
        continue
