'''
Modified: 30 January 2026
By: Ahmet Kaya

Purpose: Run our Gamification Project

Citations:
Some functions and syntax were taken from Google
Some of the code was sourced from the pad4pi GitHub and edited for use in this project
Some of the code was sourced from my Failure Fest Project and edited for use in this project
'''

from machine import Pin, PWM, I2C, ADC
from pico_i2c_lcd import I2cLcd
from pad4pi import rpi_gpio

photoresistor_pin = 1 # Subject to change
lcd_sda_pin = 12 # Subject to change
lcd_scl_pin = 13 # Subject to change
row_pins = [4, 14, 15, 17] # Subject to change
col_pins = [18, 27, 22] # Subject to change

KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

# Initialize LCD
i2c = I2C(0, sda=Pin(lcd_sda_pin), scl=Pin(lcd_scl_pin), freq = 400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

def return_key(key):
    return key

lcd.putstr("Enter the desired time and hit #.")


keypress = keypad.registerKeyPressHandler(return_key)
