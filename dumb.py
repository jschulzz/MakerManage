#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import simple_watchdog_timer as swt
from time import sleep
def cb(dog):
    # When the callback gets triggered, it's good practice to pause the WDT to prevent it firing again, while you are handling the action required when it triggers
    dog.pause()

    # Do something when the WDT triggers...
    print('WDT Triggered')

    # Update / reset the internal WDT timer (dog.reset() does the same), this is important to avoid the time spent in the callback to influence the next triggering
    dog.update()

    # Resume the WDT
    dog.resume()

reader = SimpleMFRC522()

try:
    wdt = swt.WDT(check_interval_sec=0.01, trigger_delta_sec=5, callback=cb)
    print("test1")
    id, text = reader.read()ssh
    print("test2")
    print(id)
    print(text)
    wdt.update()
finally:
    GPIO.cleanup()