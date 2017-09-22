import network
import time
import math
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

do_connect()

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
        print('Button pressed!')
        time.sleep_ms(2000)
        button_pressed = False
    else:
        pulse(led, 25)
