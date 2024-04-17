![sploosh](/Splooshtest.jpg)

[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UCz5BOU9J9pB_O0B8-rDjCWQ?style=flat&logo=youtube&logoColor=red&labelColor=white&color=ffed53)](https://www.youtube.com/channel/UCz5BOU9J9pB_O0B8-rDjCWQ) [![Instagram](https://img.shields.io/github/stars/veebch?style=flat&logo=github&logoColor=black&labelColor=white&color=ffed53)](https://www.instagram.com/v_e_e_b/)


# Clive Moss (the Window-Box Boss)

A [proportional integral derivative](https://en.wikipedia.org/wiki/PID_controller) (PID) controller that will be used to run a plant waterer. PID is a fancy way of saying that the code plays a game of 'Warmer', 'Colder' to get something to a particular value (in our example, a particular moistness). The internet is littered with examples of these things, so it is mostly a learning exercise that will use a few bits of code we've previously developed, and hopefully it will make us a little smarter along the way. This is a very lightly tweaked version of the code we used for [cooking](https://github.com/veebch/heat-o-matic).

(There's also a bare-bones version in the repository that doesn't use a screen or encoder, and has a target moisture level that can be adjusted by setting a paramater in the code. This lower-power version can be ran from a battery for extended periods of time. This is the version used in the video)


# Hardware

- Raspberry Pi Pico 
- SSD1351 Waveshare OLED (not needed if you're making the bare bones version)
- WGCD KY-040 Rotary Encoder (not needed if you're making the bare bones version)
- A **capacitive** soil-moisture sensor
- A relay switch
- A plug socket for the water pump
- A cheap fish tank water pump

**Warning: Don't pump water using something that dislikes being power-cycled a lot. This is GPL code, ie NO WARRANTY**

## Wiring

All of the pins are listed in main.py. 
GPIO to peripherals as follows:

| [Pico GPIO](https://www.elektronik-kompendium.de/sites/raspberry-pi/bilder/raspberry-pi-pico-gpio.png) | OLED |
|-----------|------|
|   19       | DIN/MOSI  |
|   18      | CLK/SCK  |
|   17      | CS  |
|   20       | DC  |
|   21      | RST  |

(not needed if you're making the bare bones version)


| [Pico GPIO](https://www.elektronik-kompendium.de/sites/raspberry-pi/bilder/raspberry-pi-pico-gpio.png) | Rotary Encoder |
|-----------|----------------|
|   2       | CLK            |
|   3       | DT             |
|   4       | SW             |

(not needed if you're making the bare bones version)


| [Pico GPIO](https://www.elektronik-kompendium.de/sites/raspberry-pi/bilder/raspberry-pi-pico-gpio.png) | Relay |
|-----------|----------------|
|   15       | Signal        |


| [Pico GPIO](https://www.elektronik-kompendium.de/sites/raspberry-pi/bilder/raspberry-pi-pico-gpio.png) | Soil Sensor |
|-----------|----------------|
|   26       | A0             |

## Enclosure

The stl files for an enclosure are on thingiverse [here](https://www.thingiverse.com/thing:6125748) (Thanks Ryan!).

# Firmware

## Installing onto a Pico

First flash the board with the latest version of micropython. 

Then clone this repository onto your computer

     git clone https://github.com/veebch/sploosh

and move into the repository directory

     cd sploosh

If (**and only if**) you are using the bare-bones version (no screen or rotary encoder)

     mv main.py withscreen.py
     mv barebones.py main.py

There are a few files to copy to the pico, [ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) is a good way to do it.

     ampy -p /dev/ttyACM0 put ./
     
substitute the device name to whatever the pico is on your system. 

# Running

Plug it in, pop the soil probe into the medium you are going to water, plug the watering device into the plug socket, pick a setpoint using the dial. That's it!

# Video

Here's a video outlining how it works and a timelapse of it looking after a plant for a week:

[![Mod demo](http://img.youtube.com/vi/WVijoh-hqkw/0.jpg)](http://www.youtube.com/watch?v=WVijoh-hqkw "Video Title")

# Contributing to the code

If you look at this and feel like you can make it better, please fork the repository and use a feature branch. Pull requests are welcome and encouraged.

# Licence 
GPL 3.0
