from qhue import Bridge
from pyW215 import SmartPlug, ON, OFF
import network
import time
import os
import pickle
import math
import gc
from machine import PWM
from machine import Pin

# Set up WiFi
def do_connect():
    # Get ap/sta state
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    # Disable AP
    ap_if.active(False)
    # Connect to the WiFi
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('SSID', 'password')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

# Callback function for button down interrupt
def button_down(p):
    global button_pressed
    if D2.value():
        button_pressed = True

# PWM pulse function
def pulse(l, t):
    for i in range(20):
        l.duty(int(math.sin(i/10*math.pi)*500+500))
        time.sleep_ms(t)

def cycle():
    # Turn switch on and off
    try:
        for i in range(0,3):
            # Get values if available otherwise return N/A
            print("State: %s" % sp.state)
            if sp.state == "ON":
                sp.state = OFF
            else:
                sp.state = ON
            time.sleep(5)
    finally:
        # cache this for later
        output = open(creds_file, 'wb')
        pickle.dump(sp.authenticated, output)
        output.close()
        print("Saved Credentials to cache")

# Be the life of the party!
def party_slut():
    try:
        for i in range(0,2):
            for color in colorlist:
                bridge.lights[8].state(on=True, bri=255, sat=255, hue=color, transitiontime=0)
                time.sleep(0.188)
        bridge.lights[8].state(**before)
    except:
        bridge.lights[8].state(**before)

do_connect()

# Setup hue stuff
BRIDGE_IP = '192.168.99.160'
USER = '2UqWouPgji3QY-PcoqakTsIRx0MQdY7LVEL3tptj'

bridge = Bridge(BRIDGE_IP, USER)

# Colors
ORANGE = 6000
YELLOW = 14500
GREEN = 26000
BLUE = 46920
PURPLE = 49000
PINK = 56100
RED = 65280

colorlist = [YELLOW, BLUE, RED, GREEN, PINK, ORANGE, PURPLE]

before = bridge.lights[8]()['state']
del before['colormode']
del before['reachable']

# Setup SmartPower
creds_file = "/tmp/creds.txt"
try:
    infile = open(creds_file, 'r')
    creds = pickle.load(infile)
    print("Credentials loaded from cache")
    infile.close()
except:
    print("No cached Credentials")
    creds = None

sp = SmartPlug('192.168.99.185', '857947', 'admin', True, auth=creds)

# Setup pins
# D1 is the button switch
D1 = Pin(5, Pin.IN)
D1.irq(trigger=Pin.IRQ_RISING, handler=button_down)
# D2 is the activation key switch
D2 = Pin(4, Pin.IN)
# Setup the button's LED
led = PWM(Pin(14), freq=1000)
led.duty(0)

button_pressed = False

while True:
    if not D2.value():
        led.duty(0)
        time.sleep_ms(5)
    elif button_pressed:
        led.duty(1023)
        #party_slut()
        cycle()
        button_pressed = False
    else:
        pulse(led, 25)
