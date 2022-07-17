![sploosh](/sploosh.jpg)

[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?label=YouTube&style=social)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ)

# Sploosh

A [proportional integral derivative](https://en.wikipedia.org/wiki/PID_controller) (PID) controller that will be used to run a plant waterer. PID is a fancy way of saying that the code plays a game of 'Warmer', 'Colder' to get something to a particular value (in our example, a particular moistness). The internet is littered with examples of these things, so it is primarily a didactic exercise that will use a few bits of code we've previously developed, and hopefully it will make us a little smarter along the way.


# Hardware

- Raspberry Pi Pico 
- SSD1351 Waveshare OLED 
- WGCD KY-040 Rotary Encoder
- AZ-Delivery Soil Capacitance Sensor
- A relay switch
- A plug socket for the water pump
- Wires Galore

**Warning: Don't pump water using something that dislikes being power-cycled a lot. This is GPL code, ie NO WARRANTY**

# Installing sploosh onto a Pico

First flash the board with the latest version of micropython. 

Then clone this repository onto your computer

     git clone https://github.com/veebch/sploosh

and move into the repository directory

     cd sploosh

There are a few files to copy to the pico, [ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) is a good way to do it.

     sudo ampy -p /dev/ttyACM0 put ./
     
substitute the device name to whatever the pico is on your system.

# Wiring

All of the pins are listed in main.py. Note that the temperature sensor needed a pull-up resistor on the signal. Also, the switch on the roatary encoder (that was being used as a means to toggle the UI) is disabled as it was being triggered by the relay.... this can probably be fixed with a capacitor. 

TO DO: Draw wiring diagram.

# Using sploosh

Plug it in, pop the soil probe into the medium you are going to water, plug the watering device into the plug socket, pick a setpoint using the dial. That's it!


# Contributing to the code

If you look at this and feel like you can make it better, please fork the repository and use a feature branch. Pull requests are welcome and encouraged.

# Licence 
GPL 3.0
