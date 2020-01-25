#!/usr/bin/env python

import RPi.GPIO as GPIO
import mfrc522

reader = SimpleMFRC522()
print(reader.READER.Read_MFRC522(self, CommandReg))

GPIO.cleanup()