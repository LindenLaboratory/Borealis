# The Borealis Network
Borealis is a network designed to automate parallel processing and multi-computer control, running in the background of Windows computers to allow the devices connected to be used as normal while their computing power is used to complete the tasks they are given. The Borealis network contains 3 types of devices:
- the _Conductor_ which gives commands
- the _Choir_ which distributes the software that receives them in HID mode and acts as an IoT device than can communicate with the conductor in FEEDBACK.
- the _Composer_ which receives commands over the intenet via Telegram and transmits them to the _Conductor_

It also contains the _Audience_ which is a program which fetches and logs the _Conductor_'s data.

---

## Borealis Devices

### Conductor
- The _Conductor_ is the first device that makes up the network
- The _Conductor_ encrypts instructions and distributes them out to the _Associate[s]_ via web server on a privately hosted WiFi network
- Instruction encryption & formatting is done with the **Eos*** Protocol

### Choir
- The _Choir_ is the second type of device making up the network
- There will usually be more than one _Choir_ device on the network
- _Choir_ devices have two modes:
    - **HID Mode**
        - The _Choir_ do not receive or process any commands
        - They only work on computers that use the Windows OS
        - When plugged into a computer it uses HID copy over the **Borealis** folder to the target computer and execute the program
        - Once it is done (3-6s) the device can be disconnected
        - This allows the _Choir_ to run on the computer with no external devices connected
    - **FEEDBACK Mode**
        - The _Choir_ now sends data to the _Conductor_
        - The data is formatted as JSON and can add commands or log data with extra functionality easy to add from _main.py_ in _Conductor_. 

### Composer
- The _Composer_ is the third and final device making up the network
- The _Composer_ connects to a Telegram Bot and receives commands over the internet before transmitting them to the _Conductor_
- This allows the network to be accessed remotely and also allows you to execute commands on multiple Borealis networks at once, allowing you to use multiple locations at any one time.
---

## Device Hardware

### Conductor
- The _Conductor_ runs on a Raspberry Pi Pico WH
- The Pico is attatches to a breadboard and the 12 and 13 pins are connected to 2 tactile buttons in order to convert to termination (red) or command terminal (green) modes
- It also has two LEDs that are not required but increase the aesthetics

|![WhatsApp Image 2024-05-22 at 07 12 53](https://github.com/LindenLaboratory/Borealis/assets/134805131/91e96973-261a-4a66-8a9f-2fbef3004be1) |
|-|

### Choir
- The _Choir_ devices run on Raspberry Pi Pico WHs
- They are connected to Adafruit Proto Under Plate PiCowBells that allow you to make IoT devices for FEEDBACK mode more easily while still maintaining the small form factor
- They connect to computers via usb-to-microusb dongles

|![WhatsApp Image 2024-05-22 at 07 13 18](https://github.com/LindenLaboratory/Borealis/assets/134805131/af757cbc-e3f0-47ea-8855-9352ee12a80e) |
|-|

### Composer
- The _Composer_ runs on a Raspberry Pi Pico WH
- The Pico is attatches to a breadboard and the 12 and 13 pins are connected to 2 tactile buttons in order to fetch network password (blue) or disable the device (yellow)
- It also has two LEDs that are not required but increase the aesthetics

| ![WhatsApp Image 2024-06-07 at 19 14 10](https://github.com/LindenLaboratory/Borealis/assets/134805131/cf6b4b1c-9a3c-49d4-9464-11070ad659e7) |
|-|

---

## Eos* Protocol

### Encryption Table
| Key | Value | Key | Value | Key | Value | Key | Value |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 00 | a | 14 | k | 32 | u | 50 |
| 1 | 01 | b | 15 | l | 33 | v | 51 |
| 2 | 02 | c | 20 | m | 34 | w | 52 |
| 3 | 03 | d | 21 | n | 35 | x | 53 |
| 4 | 04 | e | 22 | o | 40 | y | 54 |
| 5 | 05 | f | 23 | p | 41 | x | 55 |
| 6 | 10 | g | 24 | q | 42 | :. | :. |
| 7 | 11 | h | 25 | r | 43 | ;, | ;, |
| 8 | 12 | i | 30 | s | 44 |  |  |
| 9 | 13 | j | 31 | t | 45 |  |  |

### Format

1. Commands are formatted with a *prefix* and a *suffix*
    1. The p*refix* is the command that the slave devices run
    2. The *suffix* is the parameter(s) that the command takes
    3. The *prefix* and *suffix* are separated by the symbol :.
2. Commands are separated by the symbol ;,
3. Commands are Encrypted into base 6 (see Encryption Table)
    1. This is so that commands are not initially identifiable
        1. However, the encryption method used is simple as the commands are not valuable information
4. In the *suffix*, new lines are separated by “//”
    1. This is seen only with the *prefix “*code*”*
        1. In “code”, params are separated by “n”

### Prefixes
| Prefix | Function | Prefix | Function |
| --- | --- | --- | --- |
| type | Types out string | mousemove | Moves mouse to specified coordinates |
| keypress | Presses specified keys | oscmd | Runs specified OS commands |
| mouseclick | Clicks specified mouse side (left/right) | code | Runs specified python code & returns result |
| filescrape | Returns the locations of all files of a specific type with a specific keyword inside | encryptfile | Encrypts a specified file using a specific key |
| keyboardlog | Logs all keys pressed in a specific timeframe | decryptfile | Decrypts a specified file using a specific key |
| passgrab | Returns all accounts saved to google and their associated passwords as well as wifi password | mockery | Sets volume to specified value, plays video (default is "Smooth Criminal") and crashes computer |
| terminate | Removes all evidence of the virus within the specified number of seconds | datagrab | Returns gps coordinates, screenshot of current screen, ip address, mac address and device model |

---
*Efficient Orchestration System
**Bluetooth Low Energy
***Human Interface Device
