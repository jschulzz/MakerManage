### https://www.glennklockwood.com/electronics/hd44780-lcd-display.html
### https://pinout.xyz/pinout/pin40_gpio21
### https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
### https://pimylifeup.com/raspberry-pi-lcd-16x2/
### Used for reference

def LCD(textInput):

    ### Import Adafruit Python library for 16x02 LCD
    import Adafruit_CharLCD as LCD
    import time

    ### Intialize GPIO Pins being used.
    lcd_rs        = 5
    lcd_en        = 6
    lcd_d4        = 13
    lcd_d5        = 19

    lcd_d6        = 26
    lcd_d7        = 12
    lcd_backlight = 4
    lcd_columns = 16
    lcd_rows = 2

    lcd_columns = 16
    lcd_rows = 2

    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

    if len(textInput) > 32:
        lcd.message(textInput)
        for i in range(0,len(textInput)/2):
            lcd.move_left()
            time.sleep(1)
    else:
        lcd.clear()
        text = textInput
        lcd.message(text)