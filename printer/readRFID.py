#!/usr/bin/env python


def readRFID():

    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522
    #import spidev
    #spi = spidev.SpiDev()

    
    reader = SimpleMFRC522()
    try:
        id, text = reader.read_no_block()
        return id
    except:
        return None
    finally:
        GPIO.cleanup()
        #spi.close()
