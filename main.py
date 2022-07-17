# main.py - a script for making a temperature regulating PID, running using a Raspberry Pi Pico
# First prototype is using an OLED, rotary encoder and a relay switch (linked to heating device of some sort)
# The display uses drivers made by Peter Hinch [link](https://github.com/peterhinch/micropython-nano-gui)

# Released under the GPL 3.0

# Fonts for Writer (generated using https://github.com/peterhinch/micropython-font-to-py)
import gui.fonts.freesans20 as freesans20
import gui.fonts.quantico40 as quantico40
from gui.core.writer import CWriter
from gui.core.nanogui import refresh
import utime
from machine import Pin,I2C, SPI,ADC
from rp2 import PIO, StateMachine, asm_pio
import sys
import math
import gc
# Display setup
from drivers.ssd1351.ssd1351_16bit import SSD1351 as SSD

def splash(string):
    wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(50,50,0),bgcolor=0, verbose=False )
    CWriter.set_textpos(ssd, 90,25)
    wri.printstring('veeb.ch/')
    ssd.show()
    utime.sleep(.3)
    for x in range(10):
        wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(25*x,25*x,25*x),bgcolor=0, verbose=False)
        CWriter.set_textpos(ssd, 55,25)
        wri.printstring(string)
        wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(50-x,50-x,0),bgcolor=0, verbose=False )
        CWriter.set_textpos(ssd, 90,25)
        wri.printstring('veeb.ch/')
        ssd.show()
    utime.sleep(2)
    for x in range(10,0,-1):
        wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(25*x,25*x,25*x),bgcolor=0, verbose=False)
        CWriter.set_textpos(ssd, 55,25)
        wri.printstring(string)
        wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(50-x,50-x,0),bgcolor=0, verbose=False )
        CWriter.set_textpos(ssd, 90,25)
        wri.printstring('veeb.ch/')
        ssd.show()
    wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(50,50,0),bgcolor=0, verbose=False )
    CWriter.set_textpos(ssd, 90,25)
    wri.printstring('veeb.ch/')
    ssd.show()
    utime.sleep(.3)   
    return


def encoder(pin):
    # get global variables
    global counter
    global direction
    global outA_last
    global outA_current
    global outA
    
    # read the value of current state of outA pin / CLK pin
    try:
        outA_current = outA.value()
    except:
        print('outA not defined')
        outA_current = 0
        outA_last = 0
    # if current state is not same as the last stare , encoder has rotated
    if outA_current != outA_last:
        # read outB pin/ DT pin
        # if DT value is not equal to CLK value
        # rotation is clockwise [or Counterclockwise ---> sensor dependent]
        if outB.value() != outA_current:
            counter += .5
        else:
            counter -= .5
        
        # print the data on screen
        #print("Counter : ", counter, "     |   Direction : ",direction)
        #print("\n")
    
    # update the last state of outA pin / CLK pin with the current state
    outA_last = outA_current
    counter=min(9,counter)
    counter=max(0,counter)
    return(counter)
    

# interrupt handler function (IRQ) for SW (switch) pin
def button(pin):
    # get global variable
    global button_last_state
    global button_current_state
    global powerup
    if button_current_state != button_last_state:
        utime.sleep(.2)       
        button_last_state = button_current_state
#        powerup = not powerup                    # Toggle power flag - disabled for now
        print('Button:'+str(powerup))
    return

# Screen to display on OLED during heating
def displaynum(num,temperature):
    #This needs to be fast for nice responsive increments
    #100 increments?
    ssd.fill(0)
    delta=num-temperature
    text=SSD.rgb(0,255,0)
    if delta>=.5:
        text=SSD.rgb(165,42,42)
    if delta<=-.5:
        text=SSD.rgb(0,255,255)
    wri = CWriter(ssd,quantico40, fgcolor=text,bgcolor=0)
    CWriter.set_textpos(ssd, 50,0)  # verbose = False to suppress console output
    wri.printstring(str("{:.0f}".format(num)))
    wrimem = CWriter(ssd,freesans20, fgcolor=SSD.rgb(255,255,255),bgcolor=0)
    CWriter.set_textpos(ssd,100 ,0)  
    wrimem.printstring('now at: '+str("{:.0f}".format(temperature))+"/ 10")
    CWriter.set_textpos(ssd, 0,0)
    wrimem = CWriter(ssd,freesans20, fgcolor=SSD.rgb(155,155,155),bgcolor=0)
    wrimem.printstring('moisture')
    CWriter.set_textpos(ssd, 20,0)  
    wrimem.printstring('target:') 
    ssd.show()
    return

def beanaproblem(string):
    refresh(ssd, True)  # Clear any prior image
    wri = CWriter(ssd,freesans20, fgcolor=SSD.rgb(25*x,25*x,25*x),bgcolor=0, verbose=False)
    CWriter.set_textpos(ssd, 55,25)
    wri.printstring(string)
    ssd.show()
    relaypin = Pin(15, mode = Pin.OUT, value =0 )
    utime.sleep(2)
    
    
# define encoder pins 

switch = Pin(4, mode=Pin.IN, pull = Pin.PULL_UP) # inbuilt switch on the rotary encoder, ACTIVE LOW
outA = Pin(2, mode=Pin.IN) # Pin CLK of encoder
outB = Pin(3, mode=Pin.IN) # Pin DT of encoder
# Attach interrupt to Pins

# attach interrupt to the outA pin ( CLK pin of encoder module )
outA.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING,
              handler = encoder)

# attach interrupt to the outB pin ( DT pin of encoder module )
outB.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING ,
              handler = encoder)

# attach interrupt to the switch pin ( SW pin of encoder module )
switch.irq(trigger = Pin.IRQ_FALLING ,
           handler = button)


# Look for soil moisture sensor (add OLED complaint if one can't be seen)

height = 128  
pdc = Pin(20, Pin.OUT, value=0)
pcs = Pin(17, Pin.OUT, value=1)
prst = Pin(21, Pin.OUT, value=1)
spi = SPI(0,
                  baudrate=10000000,
                  polarity=1,
                  phase=1,
                  bits=8,
                  firstbit=SPI.MSB,
                  sck=Pin(18),
                  mosi=Pin(19),
                  miso=Pin(16))
gc.collect()  # Precaution before instantiating framebuf

ssd = SSD(spi, pcs, pdc, prst, height)  # Create a display instance

splash("sploosh")

# Define relay and LED pins

ledPin = Pin(25, mode = Pin.OUT, value = 0) # Onboard led on GPIO 25


# define global variables
counter = 0   # counter updates when encoder rotates
direction = "" # empty string for registering direction change
outA_last = 0 # registers the last state of outA pin / CLK pin
outA_current = 0 # registers the current state of outA pin / CLK pin

button_last_state = False # initial state of encoder's button 
button_current_state = "" # empty string ---> current state of button

# Read the last state of CLK pin in the initialisaton phase of the program 
outA_last = outA.value() # lastStateCLK

# interrupt handler function (IRQ) for CLK and DT pins


# Main Logic
pin=0
counter= 6
integral = 0
lastupdate = utime.time()  
refresh(ssd, True)  # Initialise and clear display.
wetness = machine.ADC(26)
lasterror = 0
# The Tweakable values that will help tune for our use case. TODO: Make accessible via menu on OLED
checkin = 5
# Stolen From Reddit: In terms of steering a ship:
# Kp is steering harder the further off course you are,
# Ki is steering into the wind to counteract a drift
# Kd is slowing the turn as you approach your course
Kp=2   # Proportional term - Basic steering (This is the first parameter you should tune for a particular setup)
Ki=0   # Integral term - Compensate for heat loss by vessel
Kd=0  # Derivative term - to prevent overshoot due to inertia - if it is zooming towards setpoint this
         # will cancel out the proportional term due to the large negative gradient
output=0
offstate=False
# PID loop - Default behaviour
powerup = True
while True:
    if powerup:
        try:
            counter=encoder(pin)
            # Get wetness
            howdry = 10-round(10*wetness.read_u16()/65536)
            print(howdry)
            temp = howdry # Wetness
            displaynum(counter,float(temp))
            button_last_state = False # reset button last state to false again ,
                                      # totally optional and application dependent,
                                      # can also be done from other subroutines
                                      # or from the main loop
            now = utime.time()
            dt= now-lastupdate
            if output<100 and offstate == False and dt > checkin * round(output)/100 :
                relaypin = Pin(15, mode = Pin.OUT, value =0 )
                offstate= True
                utime.sleep(.1)
            if dt > checkin:
                error=counter-temp
                integral = integral + dt * error
                derivative = (error - lasterror)/dt
                output = Kp * error + Ki * integral + Kd * derivative
                print(str(output)+"= Kp term: "+str(Kp*error)+" + Ki term:" + str(Ki*integral) + "+ Kd term: " + str(Kd*derivative))
                output = max(min(100, output), 0) # Clamp output between 0 and 100
                if error>.5:
                    output=100
                print(output)
                if output>0:  
                    relaypin = Pin(15, mode = Pin.OUT, value =1 )
                    offstate = False
                else:
                    relaypin = Pin(15, mode = Pin.OUT, value =0 )
                    offstate = True
                utime.sleep(.1)
                lastupdate = now
                lasterror = error
        except Exception as e:
            # Put something to output to OLED screen
            beanaproblem('error.')
            print('error encountered:'+str(e))
            utime.sleep(checkin)
    else:
        if button_last_state == False:  # To prevent clearing on every cycle when power off
            refresh(ssd, True)  # Clear any prior image
            relaypin = Pin(15, mode = Pin.OUT, value =0 ) 
        
