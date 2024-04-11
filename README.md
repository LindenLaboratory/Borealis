# Borealis
Borealis is a network designed to automate parallel processing and multi-computer control without needing a wifi network. The Borealis network contains 3 types of devices. See the descriptions of these below.

## Borealis Devices

### Conductor
- The _Conductor_ is the first device that makes up the network
- The _Conductor_ encrypts instructions and distributes them out to the _Associate[s]_ via web server on a privately hosted WiFi network
- Instruction encryption & formatting is done with the **Eos*** Protocol

### Associate[s]
- The _Associate_ is the second device that makes up the network
- There will usually be more than one _Associate_ on the network
- _Associates_ connect to the _Conductor_ and receive instructions
- They then transmit these instructions over a small range using BLE** and the instructions are received by the _Choir_/Computers
- With several _Associates_ the range from the group covers a large area

### Choir
- The _Choir_ is the final type of device making up the network
- There will usually be more than one _Choir_ device on the network
- The _Choir_ devices have two modes:
#### HID Mode
1. HID*** Mode requires the Choir device to be actively connected to the Computer
2. It works with any computer, from Macbook to PC to Chromebook
3. It receives instructions directly from the _Conductor_, processes them to discard any commands that do not involve keyboard or mouse and then executes them accordingly on the computer
4. It does not utilise the _Associate[s]_, skipping it entirely
#### Software Mode
1. Software Mode does not receive or process any commands
2. It only works on computers that use the Windows OS
3. When plugged into a computer it uses HID to download the Borealis exe from this repo and running it, receiving commands from the _Choir_ BLE** and running them
4. Once it is done (5-10s) the device can be disconnected
5. This allows Software Mode to run on the computer with no external devices connected and execute all non-keyboard/mouse commands

## Eos* Protocol

## Encryption Table
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

---

## Format

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

## Prefixes
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
