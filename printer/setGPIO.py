def set_pin(pin, value):
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, GPIO.LOW if value is 0 else GPIO.HIGH)
    
    #GPIO.cleanup()