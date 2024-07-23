# What is FEEDBACK Mode?
- FEEDBACK Mode is a mode of the Choir device that allows it to work as an IoT application, sending data to the Conductor
- This can be useful if you have a sensor picking up data that you need to send back, or for many other IoT purposes
# Projects
## Sensor Project
- For this you need a sensor that picks up data you wish to record, a Pico WH running the _Choir_ software (optionally connected to a Pico Proto Underplate) and enough cables for all of the pins on the sensor
- Connect the right pins on the sensor to their pico eqivalents
- Modify the base FEEDBACK code to get the data from the sensor and use that as the information to send back to the _Conductor_
## Borealis Console
- For this you need 1x [1.3" OLED Display Module for Raspberry Pi Pico (64×128)](https://thepihut.com/products/1-3-oled-display-module-for-raspberry-pi-pico-64x128) and a Pico WH running the _Choir_ software
- Plug all the pins of the pico into the corresponding sockets in the display module
- Program the _Choir_ device to scrape the _Conductor_'s server, specifically the log (located at /log) and get the final 10 lines
- Program the display's **button 0** to cycle through these, displaying one line on the screen at a time, and its **button 1** to turn on response mode	- Program the display's **button 0** to cycle through these, displaying one line on the screen at a time, and its **button 1** to switch modes to and from response mode
  - This will cycle through a predeturmined list of 10 responses instead and another click of the same button will send the currenly selected one
