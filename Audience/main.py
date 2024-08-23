#IMPORTS
import requests
import subprocess
import os
import tkinter as tk
import time

#SETUP
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
name = "Borealis"

#FUNCTIONS
def connect():
    """
    Connect to Borealis
    """
    if not os.path.isfile("borealis.xml"):
        with open("borealis.xml","w") as f:
            XML = f"""<?xml version="1.0"?>
            <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                <name>Borealis</name>
                <SSIDConfig>
                    <SSID>
                        <name>{name}</name>
                    </SSID>
                </SSIDConfig>
                <connectionType>ESS</connectionType>
                <connectionMode>auto</connectionMode>
                <MSM>
                    <security>
                        <authEncryption>
                            <authentication>WPA2PSK</authentication>
                            <encryption>AES</encryption>
                            <useOneX>false</useOneX>
                        </authEncryption>
                        <sharedKey>
                            <keyType>passPhrase</keyType>
                            <protected>false</protected>
                            <keyMaterial>pico-pico</keyMaterial>
                        </sharedKey>
                    </security>
                </MSM>
                <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">
                    <enableRandomization>false</enableRandomization>
                </MacRandomization>
            </WLANProfile>
            """
            f.write(XML)
    subprocess.call('netsh wlan add profile filename="borealis.xml"', startupinfo=si)
    subprocess.call('netsh wlan add profile filename="borealis.xml"', startupinfo=si)
    subprocess.call(f"netsh wlan connect {name}", startupinfo=si)
    time.sleep(5)

class Audience:
    def __init__(self, root, width: int, height: int):
        """
        Controls the GUI of the audience program
        :param root: tk.Tk() object
        :param width: Width of window
        :param height: Height of window
        """
        self.root = root
        self.root.title("Audience")
        self.root.configure(bg="#2b2b2b")
        self.root.geometry(f"{width}x{height}")
        self.file_location = tk.StringVar()
        self.interval = tk.StringVar()
        self.name = tk.StringVar()
        self.include_timestamp = tk.BooleanVar()
        self.create_widgets()
        root.mainloop()

    def create_widgets(self):
        """
        Creates widgets
        """
        #FRAMEa
        self.framea = tk.Frame(self.root, bg="#2b2b2b")
        self.framea.pack(pady=10)
        file_label = tk.Label(self.framea, text="Log Directory:", bg="#2b2b2b", fg="#ffffff",font=("Consolas",12),width=15)
        file_label.pack(side=tk.LEFT)
        self.file_entry = tk.Entry(self.framea, width=50, bg="#3b3b3b", fg="#ffffff", textvariable=self.file_location,
                                   font=("Consolas",12))
        self.file_entry.pack(side=tk.LEFT, padx=10)
        #FRAMEb
        self.frameb = tk.Frame(self.root, bg="#2b2b2b")
        self.frameb.pack(pady=10)
        interval_label = tk.Label(self.frameb, text="Interval:", bg="#2b2b2b", fg="#ffffff", font=("Consolas", 12),
                                  width=15)
        interval_label.pack(side=tk.LEFT)
        self.interval_entry = tk.Entry(self.frameb, width=50, bg="#3b3b3b", fg="#ffffff", textvariable=self.interval,
                                       font=("Consolas",12))
        self.interval_entry.pack(side=tk.LEFT, padx=10)
        #FRAMEd
        self.framed = tk.Frame(self.root, bg="#2b2b2b")
        self.framed.pack(pady=10)
        name_label = tk.Label(self.framed, text="Borealis Name:", bg="#2b2b2b", fg="#ffffff", font=("Consolas", 12),
                                  width=15)
        name_label.pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.framed, width=50, bg="#3b3b3b", fg="#ffffff", textvariable=self.name,
                                       font=("Consolas",12))
        self.name_entry.pack(side=tk.LEFT, padx=10)
        #FRAMEc
        self.framec = tk.Frame(self.root, bg="#2b2b2b")
        timestamp_checkbox = tk.Checkbutton(self.framec, text="Include Timestamp", variable=self.include_timestamp,
                                            bg="#4b4b4b", fg="#ffffff", selectcolor="#3b3b3b",font=("Consolas",12),
                                            borderwidth=4, relief="raised",width=30)
        submit_button = tk.Button(self.framec, text="Start", command=self.submit_fields, bg="#4b4b4b", fg="#ffffff",
                                  width=20,font=("Consolas",12), borderwidth=3, relief="raised")
        submit_button.pack(side=tk.LEFT,padx=10,pady=20)
        timestamp_checkbox.pack(side=tk.RIGHT,padx=10,pady=20)
        self.framec.pack(pady=10)

    def submit_fields(self):
        """
        Formats submitted text
        """
        try:
            global name
            file = self.file_location.get()
            interval = float(self.interval.get())
            name = self.name.get()
            timestamp = self.include_timestamp.get()
        except:
            self.root.after(2500, exit)
            framelst = [self.framea, self.frameb, self.framed, self.framec]
            for frame in framelst:
                frame.destroy()
            frame = tk.Frame(self.root, bg="#4b4b4b")
            frame.pack(padx=20, pady=20, fill="both", expand=True)
            self.text = tk.Text(frame, bg="#4b4b4b", borderwidth=4, relief="sunken", font=("Consolas", 15), fg="#ffffff")
            self.text.insert(tk.END, "Error: Incorrect entries for one or more fields. Make sure you enter a number "
                                     "for the field 'Interval'!")
            self.text.config(state="disabled")
            self.text.pack(fill="both", expand=True)
        framelst = [self.framea, self.frameb, self.framed, self.framec]
        for frame in framelst:
            frame.destroy()
        frame = tk.Frame(self.root, bg="#4b4b4b")
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.text = tk.Text(frame, bg="#4b4b4b", borderwidth=4, relief="sunken", font=("Consolas", 15), fg="#ffffff")
        self.text.insert(tk.END, f"Audience is now running. Data is being logged in {file} every {interval}s. Press "
                                 f"'Esc' to close audience or 'Enter' to reconnect to Borealis on the event of the "
                                 f"network restarting.")
        self.text.config(state="disabled")
        self.text.pack(fill="both", expand=True)
        self.root.bind("<KeyPress>", self.keypress)
        self.run(file, interval, timestamp)

    def keypress(self,event):
        """
        Detects key presses to shut down audience or reconnect to wifi
        """
        if event.keysym == "Escape":
            self.root.after(2500,exit)
            self.text.config(state="normal")
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, "Audience shutting down...")
            self.text.config(state="disabled")
        elif event.keysym == "Enter":
            connect()

    def run(self, file: str, interval: float, timestamp: bool):
        try:
            """
            Runs Audience
            :param file: Directory to write logged information to
            :param interval: Interval between each request
            :param timestamp: Whether to log the current timestamp
            """
            connect()
            time_, url = 0, "192.168.4.1/log"
            if not os.path.isdir(file):
                os.mkdir(file)
            while True:
                num = 0
                with open(f"{file}\\log{num}.txt", "a") as f:
                    log = requests.get("http://192.168.4.1/log")
                    if timestamp:
                        time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                    total = "\n".join([",".join((i, time_)) for i in log])
                    num += 1
                    f.write(total)
                time.sleep(interval)
        except:
            print("Connection Error")

#MAINLOOP
app = Audience(tk.Tk(),600,250)
