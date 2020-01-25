#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
print(reader.READER.Read_MFRC522(self, CommandReg))

GPIO.cleanup()