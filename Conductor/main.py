#IMPORTS
import network
import time
import socket
import mode as _
import connect as __
import _thread
from machine import Pin
#SETUP
addrlst = []
with open('commands.txt',"r") as f:
    commands = f.readlines()
#FUNCTIONS
def encrypt(string):
    chartable,newstring = {"a":"14","b":"15","c":"20","d":"21","e":"22","f":"23","g":"24","h":"25","i":"30","j":"31","k":"32","l":"33","m":"34","n":"35","o":"40","p":"41","q":"42","r":"43","s":"44","t":"45","u":"50","v":"51","w":"52","x":"53","y":"54","z":"55","0":"00","1":"01","2":"02","3":"03","4":"04","5":"05","6":"10","7":"11","8":"12","9":"13",":.":":."," ":"  "},""
    for char in string:
        try:
            newstring += chartable[char]
        except:
            newstring += "&" + char
    return newstring
def terminate(seconds):
    global commands
    button = Pin(9, Pin.IN, Pin.PULL_UP)
    while True:
        if button.value() == 0:
            commands = ["terminate"]
        else:
            continue
        time.sleep(seconds)
def web_page():
    global commands
    html = ''
    for command in commands:
        html = html + encrypt(command.replace("\n","").replace("\r","")) + ";,"
        print(list(command))
    return html
def ap_mode(ssid, password):
    global addrlst
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    while ap.active() == False:
        pass
    print('IP Address To Connect to:: http://' + ap.ifconfig()[0])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    while True:
      conn, addr = s.accept()
      print('Got a connection from %s' % str(addr))
      if str(addr).split(",")[0] not in addrlst:
          addrlst.append(str(addr).split(",")[0])
      request = conn.recv(1024)
      print('Content = %s' % str(request))
      response = str(len(addrlst))+".:"+web_page()
      print(response)
      conn.send(response)
      conn.close()
#MAINLOOP
if _.var() == False:
    print("Borealis Online (acc #01)")
    _thread.start_new_thread(terminate,[0.5])
    ap_mode('Borealis',
        'pico-pico')
else:
    addcmd = __.run(commands)
    if addcmd != False:
        commands = addcmd
        print("Borealis Online (acc #02)")
        _thread.start_new_thread(terminate,[0.5])
        ap_mode('Borealis',
        'pico-pico')
    else:
        with open("commands.txt","w") as f:
            f.write("\n".join(addcmd))
        print("Borealis Offline")
