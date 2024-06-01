#IMPORTS
import subprocess, socket, time, os
from colorama import init
from termcolor import colored

#SETUP
init()
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
wait,finalwait = 1,0
with open('settings.txt','r') as f:
	lst_ = f.readlines()
	borealisname = lst_[1].replace("\n","")
	wifi = lst_[0].replace("\n","")
	coloura = lst_[2].replace("\n","")
	colourb = lst_[3].replace("\n","")
	delay = int(lst_[4].replace("\n",""))
	additional = float(lst_[5].replace("\n",""))

#FUNCTIONS
def get(url):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((url, 80))
		s.sendall(bytes(f"GET /log HTTP/1.1\r\nHost:{url}\r\n\r\n", encoding='utf-8'))
		eosstr = s.recv(4096).decode()
		s.close()
		return eosstr
	except Exception:
		return False

def ping(ip):
	global wait
	subprocess.call('netsh wlan add profile filename="borealis.xml"', startupinfo=si)
	subprocess.call(f"netsh wlan connect {borealisname}", startupinfo=si)
	if finalwait == 0: 
		wait = wait + additional
		time.sleep(wait)
	else: time.sleep(finalwait)
	result = get(ip)
	return result

def clear(exception):
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith(".txt") and filename != exception:
            os.remove(filename)

#MAINLOOP
print(colored("Press ENTER to continue or type DELETE to remove existing snapshots","light_blue"))
delete = input()
if delete.lower() == "delete":
	clear("settings.txt")
while True:
	_ = ping("192.168.4.1")
	if _ == False: 
		subprocess.call(f"netsh wlan connect {wifi}", startupinfo=si)
		time.sleep(0.5)
	else:
		os.system("cls")
		print(colored(_,"cyan"))
		timestamp = time.time()
		with open(f"{timestamp}.txt","w") as f:
			f.write(_)
		finalwait = wait
		subprocess.call(f"netsh wlan connect {wifi}", startupinfo=si)
		time.sleep(delay)