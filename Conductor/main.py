#IMPORTS
import network
import time
import socket
import mode as _
import connect as __
import _thread
from machine import Pin
import json
#SETUP
addrlst = []
with open("settings.txt","r") as f: 
    NAME = f.readline().strip()
with open('commands.txt',"r") as f:
    commands = f.readlines()
FEEDBACK = True
#FUNCTIONS
def execute(string):
    dictionary = eval(string)
    def log(dictionary):
        if "log" in dictionary:
            logstr=dictionary['log']
            with open("log.txt","r") as f:
                lines = f.readlines()
                if len(lines) < 100:
                    with open("log.txt","a") as f:
                        f.write(logstr + "\n")
                else:
                    with open("log.txt","w") as f:
                        f.write("".join(lines[1:])+logstr + "\n")
            return "Data Logged"
        else:
            return "Data Logging Failed"
    def command(dictionary):
        if "command" in dictionary:
            commandstr=dictionary['command']
            commands.append(commandstr)
            return "Command Added"
        else:
            return "Command Adding Failed"
    #ANALYSIS
    log(dictionary)
    command(dictionary)
def encrypt(string):
    pause = False
    chartable,newstring = {"a":"14","b":"15","c":"20","d":"21","e":"22","f":"23","g":"24","h":"25","i":"30","j":"31","k":"32","l":"33","m":"34","n":"35","o":"40","p":"41","q":"42","r":"43","s":"44","t":"45","u":"50","v":"51","w":"52","x":"53","y":"54","z":"55","0":"00","1":"01","2":"02","3":"03","4":"04","5":"05","6":"10","7":"11","8":"12","9":"13"," ":"  "},""
    for char in string:
        try:
            newstring += chartable[char]
        except:
            if char == ":":
                pause = True
                continue
            elif char == "." and pause == True:
                newstring += ":."
            else:
                newstring += "&" + char
    return newstring
def terminate(seconds):
    global commands
    button = Pin(19, Pin.IN, Pin.PULL_UP)
    while True:
        if button.value() == 0 and "terminate:.0" not in commands:
            commands.append("terminate:.0")
            for i in commands:
                if "oscmd" in i:
                    commands.remove(i)
        else:
            continue
        time.sleep(seconds)
def web_page():
    global commands
    html,timestamp,t__ = '','0',0
    for command in commands:
        if not "timestamp" in command and not "=" in command:
            html = html + encrypt(command.replace("\n","").replace("\r","")) + ";,"
        else:
            if "=" in command:
                t__ = int(command.split("=")[-1])
            else:
                timestamp_ = command.replace("\n","").replace("\r","").split(":.")[1]
                timestamp = t__+int(timestamp_.split("t")[-1])
    return html,timestamp
def ap_mode(ssid, password):
    global addrlst, FEEDBACK
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
      if "Adafruit CircuitPython" in str(request) and "POST" in str(request):
          if FEEDBACK:
              string = "{" + str(request).split("GET")[-1].split("{")[-1][:-1]
              print(string);execute(string)
          FEEDBACK = not FEEDBACK
      elif "Borealis Client" in str(request) and "POST" in str(request):
          string = "{" + str(request).split("GET")[-1].split("{")[-1][:-1]
          print(string);execute(string)
      htmlcontent,timestamp = web_page()
      sitedir = str(request).split(" HTTP/1.1")[0].split(" ")[1]
      print(sitedir)
      if sitedir == "/log":
          with open("log.txt","r") as f:
              response = "".join(f.readlines())
      else:
          response = str(len(addrlst))+".:"+str(timestamp)+".:"+htmlcontent
      print(response)
      response = b"""\
HTTP/1.1 200 OK
Content-Type: text/plain


"""+response
      conn.send(response)
      conn.close()
#MAINLOOP
if _.var() == False:
    print(f"Borealis Online (acc #01)\nRunning on name '{NAME}'")
    _thread.start_new_thread(terminate,[0.5])
    ap_mode(NAME,
        'pico-pico')
else:
    addcmd = __.run(commands)
    if addcmd != False:
        commands = addcmd
        print(f"Borealis Online (acc #02)\nRunning on name '{NAME}'")
        _thread.start_new_thread(terminate,[0.5])
        ap_mode(NAME,
        'pico-pico')
    else:
        with open("commands.txt","w") as f:
            f.write("\n".join(addcmd))
        print("Borealis Offline")
