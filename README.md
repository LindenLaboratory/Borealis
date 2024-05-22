# The Borealis Network
Borealis is a network designed to automate parallel processing and multi-computer control, running in the background to allow the devices connected to be used as normal while their computing power is used as they are connected to the database. The Borealis network contains 2 types of devices, the _Conductor_ which gives commands and the _Choir_ which distributes the software that receives them.

---

## Borealis Devices

### Conductor
- The _Conductor_ is the first device that makes up the network
- The _Conductor_ encrypts instructions and distributes them out to the _Associate[s]_ via web server on a privately hosted WiFi network
- Instruction encryption & formatting is done with the **Eos*** Protocol

### Choir
- The _Choir_ is the final type of device making up the network
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

---

## Device Hardware

### Conductor
- The _Conductor_ runs on a Raspberry Pi Pico WH
- The Pico is attatches to a breadboard and the 12 and 13 pins are connected to 2 tactile buttons in order to convert to termination or command terminal modes
- It also has two LEDs that are not required but increase the aesthetics
- The _Conductor_ is contained in a custom case but this is obviously not necessary

|![WhatsApp Image 2024-05-22 at 07 12 53](https://github.com/LindenLaboratory/Borealis/assets/134805131/91e96973-261a-4a66-8a9f-2fbef3004be1) |
|-|

### Choir
- The _Choir_ devices run on Raspberry Pi Pico WHs
- They are connected to Adafruit Proto Under Plate PiCowBells that allow you to make IoT devices for FEEDBACK mode more easily while still maintaining the small form factor
- They connect to computers via usb-to-microusb dongles

|![WhatsApp Image 2024-05-22 at 07 13 18](https://github.com/LindenLaboratory/Borealis/assets/134805131/af757cbc-e3f0-47ea-8855-9352ee12a80e) |
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

---
*Efficient Orchestration System
**Bluetooth Low Energy
***Human Interface Device
