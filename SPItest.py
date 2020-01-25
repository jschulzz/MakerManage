#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from mfrc522 import MFRC522
import mfrc522
reader = SimpleMFRC522()
print(reader.READER.Read_MFRC522(CommandReg))

GPIO.cleanup()