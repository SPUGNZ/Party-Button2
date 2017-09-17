#!/usr/local/bin/micropython

from qhue import Bridge
import time

BRIDGE_IP = '192.168.99.160'
USER='2UqWouPgji3QY-PcoqakTsIRx0MQdY7LVEL3tptj'

b = Bridge(BRIDGE_IP, USER)

# Colors
ORANGE = 6000
YELLOW = 14500
GREEN = 26000
BLUE = 46920
PURPLE = 49000
PINK = 56100
RED = 65280

colorlist = [YELLOW, BLUE, RED, GREEN, PINK, ORANGE, PURPLE]

before = b.lights[8]()['state']
del before['colormode']
del before['reachable']
try:
    while True:
        for color in colorlist:
            b.lights[8].state(on=True, bri=255, sat=255, hue=color, transitiontime=0)
            time.sleep(0.188)
except:
    b.lights[8].state(**before)

