#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from mfrc522 import MFRC522
import mfrc522
CommandReg = 0x01
reader = SimpleMFRC522()
reader.READER.Write_MFRC522(CommandReg,0x2F)
print(reader.READER.Read_MFRC522(CommandReg))

GPIO.cleanup()