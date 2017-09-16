#!/home/nathan/src/micropython/ports/unix/micropython
from pyW215 import SmartPlug, ON, OFF
import time, os, pickle

def cycle():
    # Turn switch on and off
    while True:
        # Get values if available otherwise return N/A
        print("Current Consumption: %s" % sp.current_consumption)
        print("State: %s" % sp.state)
        if sp.state == "ON":
            sp.state = OFF
        else:
            sp.state = ON
        time.sleep(10)

def do_stuff():
    print("State: %s" % sp.state)

creds_file = '/tmp/creds.txt'

creds = None
if os.path.exists(creds_file):
    try:
        infile = open(creds_file, 'rb')
        creds = pickle.load(infile)
        print("Credentials loaded from cache")
        infile.close()
    except:
        raise
        creds = None

sp = SmartPlug('192.168.99.199', '857947', 'admin', True, auth=creds)

try:
    do_stuff()
finally:
    # cache this for later
    output = open(creds_file, 'wb')
    pickle.dump(sp.authenticated, output)
    output.close()

