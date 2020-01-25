def set_pin(pin, value):
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, GPIO.LOW if value is 0 else GPIO.HIGH)