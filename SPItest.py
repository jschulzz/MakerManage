#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from mfrc522 import MFRC522
from time import sleep
CommandReg = 0x01
FIFODataReg = 0x09
BitFramingReg = 0x0D
reader = SimpleMFRC522()
reader.READER.Write_MFRC522(CommandReg,0x2F)
print(reader.READER.Read_MFRC522(CommandReg))

cardRead = False
      
def card_read(self):
    cardRead = True
    

def activate_transciever():
    reader.READER.Write_MFRC522(FIFODataReg, 0x26)
    reader.READER.Write_MFRC522(CommandReg, 0x0C)
    reader.READER.Write_MFRC522(BitFramingReg, 0x87)
GPIO.setup(24,GPIO.IN)
GPIO.add_event_detect(24, GPIO.FALLING,callback=card_read)

for i in range(1,100):
    if cardRead is True:
        cardRead = False
        print("A card was read!")
        id, text = reader.read()
        print(id)
        print(text)
        reader.READER.Write_MFRC522(CommIrqReg, 0x7F)
    print("hello")
    activate_transciever()
    sleep(.1)

GPIO.cleanup()