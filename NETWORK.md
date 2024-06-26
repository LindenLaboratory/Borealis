# Network
This document explains how to setup and use the borealis network

## Setup
- Setting up and using the Borealis network is quite simple
- It should take you 10-30m if you have all of the components
- You will need:
    - 2x Raspberry Pi Pico WH
    - **At Least** 1x Raspberry Pi Pico W, 1x Pico Dongle Lite & 1x Adafruit Proto Under Plate PiCowBell for Pico
    - 4x Male-to-Male Jumper Cables
    - 2x 4-Legged Tactile Switch Buttons
    - **Optional:**
        - Additional 'Raspberry Pi Pico W's, 'Pico Dongle Lite's & 'Adafruit Proto Under Plate PiCowBell for Pico's
        - 4x Additional Male-to-Male Jumper Cables for LEDs
        - 4x LEDs
        - 4x Resistors
        - ≥2x '3xAAA USB Battery Holder with Cover and Switch'
- First, set up the _Conductor_ as shown in the **Device Hardware** section of [the README](README.md).
- Next, plug the _Conductor_ into your computer and [install micropython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).
- Finally, copy over the files from the _Conductor_ directory in [Thonny](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/2).
- Setup the _Composer_ in the same way but with different coloured wires to distinguish the two, [installing circuitpython](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython) instead of micropython and copying over the files from the _Composer_ directory.
- You also need to make a telegram bot and change the bot token to your new bot's token, or you can use the default but this will connect your Borealis network to the wider internet so anyone using it will be able to access your network
- Now, to setup the _Choir_ device(s), connect a Raspberry Pi Pico to your computer via a Pico Dongle Lite and [install circuitpython](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython). Then, upload the files from the _Choir_ directory - you can do this in file manager.

## Use
- When you plug in the _Conductor_, if you are holding down the green button (see **Device Hardware**) you can use Thonny to enter new commands in the command console (see the **Eos** section of [the README](README.md)) or edit the commands.txt file directly
- If you press the red button (see **Device Hardware**) it will change the command to "terminate" and the software will stop running on all slave computers and run dormant until the computer restarts
- When you plug in the _Composer_, if you press the blue button (see **Device Hardware**) within 5 seconds of turning on the device it will use HID to get the wifi password and then will start getting any commands over telegram
- If you press the yellow button it will terminate the connection
- If you press nothing for 5 seconds it will try and use the last password that was scraped and start running but if there is no stored passwords it will continue waiting for a button press.
- To connect a computer to the network, simply plug the _Choir_ device into a computer and it will install itself. Make sure the settings.txt file has its bottom row set to **True** so that the device is in HID mode
- To remove the computer from the network, press the terminate button on the _Conductor_ and remove the **run.bat** file from startup
- Once a device is connected, it will connect to Borealis, ping the network to get its id, and then in several minutes it will start getting the commands
- If a command is in the **funcdoc.eos** file it will run it and send the result to the _Conductor_ which will then log it with a **<:** prefix and **:>** suffix to denote it as a result.
    - You can see logs at **192.168.4.1/log**
- You can also change the times between each request, the time it waits to connect to the network when pinging it, the base time when requesting, the standard wifi the computer connects to and the name of the Borealis network incase you want to change it from the conductor side.
- To run an IoT device on the network, plug the _Choir_ device into a power source (see battery holder in **_Optional_, Setup**), making sure that the settings.txt file has its bottom row set to **False** so that the device is in FEEDBACK mode. Then, edit **code.py** (see [the _Choir_ folder](Choir)) to include the code for your IoT applications, e.g reading from a temperature sensor, and to send off said data to the _Conductor_. You can either log the data (FEEDBACK logs will be denoted by a **>:** prefix and a **:<** suffix) or add a command to the commands list or, alternatively, add your own functionallity.
- Finally, to store the logs on your computer, run **main.py** (see [the _Audience_ Folder](Audience) and it will connect to the network and show the logs every 30s as well as logging them in text files labeled with their timestamps.
    - This is necessary as the _Conductor_'s log only holds 99 lines at any one time so will write over old data
