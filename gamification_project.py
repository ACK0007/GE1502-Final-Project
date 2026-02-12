'''
Modified: 12 February 2026
By: Ahmet Kaya

Purpose: Run our Gamification Project

Citations:
Some functions and syntax were taken from Google
Some of the code was sourced from the pad4pi GitHub and edited for use in this project
Some of the code was sourced from my Failure Fest Project and edited for use in this project
gpiozero documentation
'''

from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
from gpiozero import Button
from pad4pi import rpi_gpio
from servo import Servo
import time

photoresistor_pin = 1 # Subject to change
lcd_sda_pin = 12 # Subject to change
lcd_scl_pin = 13 # Subject to change
row_pins = [4, 14, 15, 17] # Subject to change
col_pins = [18, 27, 22] # Subject to change
magnetic_switch_pin = 0 # Subject to change
servo_pin = 2 # Subject to change

class Keypad():
    def __init__(self, row_pins, col_pins):
        keys = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            ["*", 0, "#"]
        ]
        factory = rpi_gpio.KeypadFactory()
        # Try factory.create_4_by_3_keypad
        # and factory.create_4_by_4_keypad for reasonable defaults
        self.keypad = factory.create_keypad(keys, row_pins, col_pins)
        
    def keypress(self):
        return self.keypad.registerKeyPressHandler(lambda key: key)



class PhoneBox():
    def __init__(self):
        self.keypad = Keypad(row_pins,col_pins)
        # Initialize LCD
        self.initialize_lcd()
        self.time: int = 0
        self.magnet = gpiozero.Button(magnetic_switch_pin, pull_up=True)
        self.lock = Servo(Pin(servo_pin))
        
        # Initializes the LCD display
    def initialize_lcd(self):
        i2c = I2C(0, sda=Pin(lcd_sda_pin), scl=Pin(lcd_scl_pin), freq = 400000)
        I2C_ADDR = i2c.scan()[0]
        self.lcd = I2cLcd(i2c, I2C_ADDR, 2, 16) # 2 rows on LCD, 16 columns
        
    def set_timer(self):
        self.lcd.putstr("Enter the desired time in minutes and hit #.")
        keypresses = []
        while keypress != "#":
            keypress = self.keypad.keypress()
            keypresses.append(keypress)
            
        for k in keypresses:
            self.time += k
            
        self.time = int(self.time)
            
    def display_countdown(self):
        while self.time != 0 and self.keypad.keypress() != "#":
            self.lcd.putstr(self.time_display_format())
            time.sleep(1)
            self.lcd.clear()
            

    def time_display_format(self):
        min = int(self.time/60)
        sec = self.time - min
        return f"{min}:{sec}"
    
    
    def run_phonebox(self):
        self.set_timer()
        self.lock.write(90)
        self.main_loop()
        
    def main_loop(self):
        self.display_countdown()
        if self.time == 0:
            self.lcd.putstr("Time's up!")
            self.lock.write(0)
        else:
            self.lcd.putstr("Why did you stop the timer")
            time.sleep(1)
            self.lcd.clear()
            pause_options = {"A": "A: Important notification", "B": "B: I give up"}
            display_string = pause_options["A"]
            while keypress := self.keypad.keypress() not in pause_options.keys():
                self.lcd.putstr("Why did you stop the timer")
                self.lcd.move_to(0,1)
                self.lcd.putstr(display_string)
                display_string = pause_options["A"] if display_string != pause_options["A"] else display_string["B"]
                time.sleep(1)
                self.lcd.clear()
            if keypress == "A":
                self.lcd.putstr("Paused due to important notification")
            elif keypress == "B":
                self.lcd.putstr("Paused due to lack of willpower")
            self.lcd.move_to(0,1)
            self.lcd.putstr("Press # to resume")
            while keypress := self.keypad.keypress() != "#":
                time.sleep(0.1)
            self.main_loop()
                
                

        