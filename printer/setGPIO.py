def set_pin(pin, value):
    from RPi.GPIO import GPIO

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(relay, GPIO.LOW if value is 0 else GPIO.HIGH)
