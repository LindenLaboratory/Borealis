#IMPORTS
import network
import time
import socket
import mode as _
import connect as __
import _thread
from machine import Pin
import json
import os
import machine

#SETUP
addrlst = []
responses = []
amounts = []
money = ""

with open("settings.txt", "r") as f:
    NAME = f.readline().strip()
    f.close()

with open('commands.txt', "r") as f:
    commands = f.readlines()
    f.close()

UPLOAD_DIR = "/app"

#FUNCTIONS
def getdata(username):
    with open("accounts.csv", "r") as f:
        lines = f.readlines()
        for i in lines:
            parts = i.replace("\n", "").split(",")
            if parts[0] == username:
                return parts
        f.close()

def execute(string):
    dictionary = eval(string)
    
    def log(dictionary):
        if "log" in dictionary:
            logstr = dictionary['log']
            with open("log.txt", "r") as f:
                lines = f.readlines()
                f.close()
                if len(lines) < 100:
                    with open("log.txt", "a") as f:
                        f.write(logstr + "\n")
                        f.close()
                else:
                    with open("log.txt", "w") as f:
                        f.write("".join(lines[1:]) + logstr + "\n")
                        f.close()
            return "Data Logged"
        else:
            return "Data Logging Failed"
    
    def command(dictionary):
        global commands
        if "command" in dictionary:
            commandstr = dictionary['command']
            commands.append(commandstr)
            return "Command Added"
        else:
            return "Command Adding Failed"
    
    def transfer(dictionary):
        try:
            if "transfer" in dictionary:
                name,target,amount = dictionary['transfer'].split(",")
                with open("accounts.csv", "r") as f:
                    lines_ = []
                    lines = f.readlines()
                    f.close()
                    for line in lines:
                        lst = line.split(",")
                        if username == lst[0]:
                            if lst[2] > amount:
                                lst[2] = lst[2] - amount
                                lines_.append(",".join(lst))
                            else:
                                return "User Info Edit Failed"
                        elif amount == lst[0]:
                            lst[2] = lst[2] + amount
                            lines_.append(",".join(lst))    
                        else:
                            lines_.append(line)
                    with open("accounts.csv","w") as f:
                        f.write("\n".join(lines_))
                        f.close()
                return "User Info Edited"
            else:
                return "User Info Edit Failed"
        except:
            return "User Info Edit Failed"

    #ANALYSIS
    print(log(dictionary),command(dictionary),transfer(dictionary))

def encrypt(string):
    pause = False
    chartable = {
        "a": "14", "b": "15", "c": "20", "d": "21", "e": "22", "f": "23",
        "g": "24", "h": "25", "i": "30", "j": "31", "k": "32", "l": "33",
        "m": "34", "n": "35", "o": "40", "p": "41", "q": "42", "r": "43",
        "s": "44", "t": "45", "u": "50", "v": "51", "w": "52", "x": "53",
        "y": "54", "z": "55", "0": "00", "1": "01", "2": "02", "3": "03",
        "4": "04", "5": "05", "6": "10", "7": "11", "8": "12", "9": "13", " ": "  "
    }
    newstring = ""
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
        elif _.var() == True:
            machine.reset()
        else:
            continue
        time.sleep(seconds)

def web_page():
    global commands
    print(commands)
    html, timestamp, t__ = '', '0', 0
    for command in commands:
        if not "timestamp" in command and not "=" in command:
            html += encrypt(command.replace("\n", "").replace("\r", "")) + ";,"
        else:
            if "=" in command:
                t__ = int(command.split("=")[-1])
            else:
                timestamp_ = command.replace("\n", "").replace("\r", "").split(":.")[1]
                timestamp = t__ + int(timestamp_.split("t")[-1])
    return html, timestamp

def ap_mode(ssid, password):
    global addrlst
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    while not ap.active():
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
        if "POST" in str(request):
            string = "{" + str(request).split("GET")[-1].split("{")[-1][:-1]
            print(string); execute(string)
        htmlcontent, timestamp = web_page()
        sitedir = str(request).split(" HTTP/1.1")[0].split(" ")[1]
        print(sitedir)
        if sitedir == "/log":
            with open("log.txt", "r") as f:
                response = "".join(f.readlines())
                f.close()
        elif "/app" in sitedir:
            if sitedir == "/app":
                response = """
<!DOCTYPE html>
<html>
<head>
    <title>Upload Files</title>
    <style>
        body { background-color: #121212; color: #ffffff; font-family: 'Nunito', sans-serif; }
        .container { max-width: 500px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; }
        .form-group input[type="file"] { display: block; }
        .form-group button { padding: 10px 20px; background-color: #262626; color: #ffffff; border: none; cursor: pointer; }
        .form-group button:hover { background-color: #3700b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Upload Files</h1>
        <form action="/app/upload" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="pyfile">Python Script:</label>
                <input type="file" id="pyfile" name="pyfile">
            </div>
            <div class="form-group">
                <button type="submit">Upload</button>
            </div>
        </form>
    </div>
</body>
</html>
"""
            elif sitedir == "/app/upload":
                request = request.decode()
                boundary = request.split("boundary=")[1].split("\r\n")[0]
                content_length = int(request.split("Content-Length: ")[1].split("\r\n")[0])
                body = conn.recv(content_length).decode()
                parts = body.split(boundary)
                for part in parts:
                    try:
                        if "Content-Disposition: form-data; name=\"pyfile\"; filename=" in part:
                            py_filename = part.split("filename=")[1].split("\r\n")[0].strip("\"")
                            py_content = part.split("\r\n\r\n")[1].rsplit("\r\n", 1)[0]
                            splitlst = py_content.split("""'''""")
                            description,content = splitlst[1],splitlst[2]
                            py_path,txt_path = f"{UPLOAD_DIR}/{py_filename}",f"{UPLOAD_DIR}/list.txt"
                            descript = description.lstrip().rstrip().replace("\n",":.").replace("\r","")+"\n"
                            print(descript+"\n\n"+content)
                            try:
                                with open(py_path, 'w') as f:
                                    f.write(content.lstrip())
                                    f.close()
                                with open(txt_path,"r") as f:
                                    if descript not in "".join(f.readlines()):
                                        f.close()
                                        with open(txt_path,"a") as f:
                                            f.write(descript)
                                        print("Python file saved successfully",py_path)
                                response = "File uploaded successfully"
                            except OSError as e:
                                print(f"Error saving Python file: {e}")
                                response = "Error 500: File save error"
                    except Exception as e:
                        print(e)
                        response = "Error 400: File formatted incorrectly"
            elif sitedir == "/app/list":
                with open(f"{UPLOAD_DIR}/list.txt","r") as f:
                    response = "".join(f.readlines())
                    f.close()
            else:
                filename = sitedir.split("/")[-1]
                try:
                    with open(f"{UPLOAD_DIR}/{filename}","r") as f:
                        response = "".join(f.readlines())
                        f.close()
                except Exception as e:
                    print(e)
                    response = "Error 404: App not found"
        elif "/account" in sitedir:
            if sitedir == "/account":
                response = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #121212;
            color: #ffffff;
            font-family: 'Nunito', sans-serif;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .input-box {
            margin: 10px 0;
            padding: 10px;
            width: 200px;
            border: 1px solid #555;
            border-radius: 5px;
            background-color: #1e1e1e;
            color: #ffffff;
            font-family: 'Nunito', sans-serif;
        }
        .button {
            margin: 10px 0;
            padding: 10px;
            width: 200px;
            border: none;
            border-radius: 5px;
            background-color: #262626;
            color: #ffffff;
            cursor: pointer;
            font-family: 'Nunito', sans-serif;
        }
        .button:hover {
            background-color: #3700b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <input id="username" class="input-box" type="text" placeholder="Username">
        <input id="password" class="input-box" type="password" placeholder="Password">
        <button class="button" onclick="login()">Login</button>
    </div>
    <script>
        function login() {
            var username = document.getElementById('username').value;
            var password = document.getElementById('password').value;
            var url = '/account?v=1&u=' + encodeURIComponent(username) + '&p=' + encodeURIComponent(password);
            window.location.href = url;
        }
    </script>
</body>
</html>
"""
            elif sitedir == "/account/save":
                print(str(request))
                string = "{" + str(request).split("{")[-1][:-1]
                dictionary = eval(string)
                username = dictionary["title"]
                text_ = dictionary["content"]
                lst = text_.split("\\n\\n")
                lst = [_.replace("\\n",":.") for _ in lst]
                lines_=[]
                with open("accounts.csv", "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if password == line.split(",")[1]:
                            other = ",".join(lst)
                            lines_.append(f"{username},{password},{money},{other}\n")
                        else:
                            lines_.append(line)
                    f.close()
                with open("accounts.csv","w") as f:
                    f.write("".join(lines_))
                    f.close()
                            
                response = "Data saved successfully"
            else:
                try:
                    response = "Success"
                    variables = sitedir.split("?")[1].split("&")
                    variables = [var.split("=")[1] for var in variables]
                    version = variables[0]
                    username = variables[1]
                    if version == "1":
                        password = variables[2]
                        with open("accounts.csv", "r") as f:
                            txt = "".join(f.readlines())
                            f.close()
                            if username in txt:
                                items = getdata(username)
                                money = items[2]
                                if items[1] != password:
                                    response = "Error: Incorrect Password"
                                else:
                                    items = [item.split(":.") for item in items[3:]]
                            else:
                                responses = ["Message " + str(i) for i in range(1, 11)]
                                amounts = [str(i) + ".00" for i in range(1, 11)]
                                items = [responses, amounts]
                                money = "2.40"
                                with open("accounts.csv", "a") as f:
                                    responses = ":.".join(responses)
                                    amounts = ":.".join(amounts)
                                    f.write(f"{username},{password},{money},{responses},{amounts}\n")
                                    f.close()
                                with open("log.txt","a") as f:
                                    f.write(f"Account '{username}' Created!\n")
                                    f.close()
                        if response != "Error: Incorrect Password":
                            text = ""
                            for lst in items:
                                for item in lst:
                                    text = text + item + "\n"
                                text += "\n"
                            text = text.rstrip()
                            response = f"""\
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Ebony Notepad</title>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Maven+Pro&display=swap">
        <style>
            body {{
                background-color: #444;
                color: #fff;
                font-family: 'Maven Pro', sans-serif;
                display: flex;
            }}

            #notepad {{
                width: 75%;
                height: 90vh;
                border: none;
                outline: none;
                resize: none;
                background-color: #333;
                color: #fff;
                padding: 20px;
                font-size: 20px;
            }}

            #taskbar {{
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                background-color: #555;
                padding: 20px;
                margin-left: 10px;
                align-items: flex-start;
                flex-wrap: wrap;
            }}

            #title {{
                font-family: 'Maven Pro', sans-serif;
                flex: 1 1 auto;
                width: 100%;
                height: 50px;
                padding: 10px;
                font-size: 25px;
                background-color: #555;
                color: #fff;
                border: none;
                outline: none;
                margin-bottom: 10px;
            }}

            #save-btn {{
                font-family: 'Maven Pro', sans-serif;
                width: 100%;
                height: 50px;
                padding: 10px 20px;
                font-size: 16px;
                background-color: #262626;
                color: #fff;
                border: none;
                cursor: pointer;
                margin-bottom: 10px;
            }}

            #money-display {{
                flex-grow: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                background-color: #555;
                color: #fff;
                text-align: center;
                font-size: 30px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <textarea id="notepad" placeholder="Start typing...">{text}</textarea>
        <div id="taskbar">
            <input type="text" id="title" placeholder="Enter a title..." value="{username}">
            <button id="save-btn">Save</button>
            <div id="money-display">£{money}</div>
        </div>
        <script>
            document.getElementById("save-btn").addEventListener("click", function() {{
                var title = document.getElementById("title").value;
                var content = document.getElementById("notepad").value;

                // Create a new XMLHttpRequest object
                var xhr = new XMLHttpRequest();

                // Configure the request
                xhr.open("POST", "/account/save", true);
                xhr.setRequestHeader("Content-Type", "application/json");

                // Define the data to be sent
                var data = JSON.stringify({{ title: title, content: content }});

                // Handle the response
                xhr.onreadystatechange = function() {{
                    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {{
                        // Handle the response from the Flask route
                        var response = JSON.parse(xhr.responseText);
                        console.log(response);
                    }}
                }};

                // Send the request with the data
                xhr.send(data);
            }});
        </script>
    </body>
</html>"""
                    else:
                        datalst = getdata(username)[2:]
                        response = "\n\n".join([item.replace(":.","\n") for item in datalst])
                except Exception as e:
                    response = "Error 400: Mistyped Address"
                    print(e)
        else:
            response = str(len(addrlst)) + ".:" + str(timestamp) + ".:" + htmlcontent
        if "</html>" not in response:
            responsefinal = f"""\
HTTP/1.1 200 OK\r
Content-Type: text/plain\r
Content-Length: {len(response)}\r
\r
{response}"""
        else:
            responsefinal = response
        conn.send(responsefinal.encode('utf-8'))
        conn.close()

#MAINLOOP
if _.var() == False:
    print(f"Borealis Online (acc #01)\nRunning on name '{NAME}'")
    _thread.start_new_thread(terminate, [0.5])
    ap_mode(NAME, 'pico-pico')
else:
    addcmd = __.run(commands)
    if addcmd != False:
        commands = addcmd
        print(f"Borealis Online (acc #02)\nRunning on name '{NAME}'")
        _thread.start_new_thread(terminate, [0.5])
        ap_mode(NAME, 'pico-pico')
    else:
        with open("commands.txt", "w") as f:
            f.write("\n".join(addcmd))
            f.close()
        print("Borealis Offline")
