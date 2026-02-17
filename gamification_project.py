'''
Modified: 17 February 2026
By: Ahmet Kaya

Purpose: Run our Gamification Project

Citations:
Some functions and syntax were taken from Google
Some of the code was sourced from the pad4pi GitHub and edited for use in this project
Some of the code was sourced from my Failure Fest Project and edited for use in this project
picozero documentation
https://nerdcave.xyz/raspberrypi/module-and-sensors/tutorial-4-keypad/
'''

from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
from picozero import Button, Servo
import time

lcd_sda_pin = 12 # Subject to change
lcd_scl_pin = 13 # Subject to change
row_pins = [4, 14, 15, 17] # Subject to change
col_pins = [18, 27, 22] # Subject to change
magnetic_switch_pin = 0 # Subject to change
servo_pin = 2 # Subject to change

class Keypad():
    def __init__(self, row_pins, col_pins):
        self.keys = ["1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "#", "D"]
        # Initialize row pins as DigitalOutputDevice
        self.rows = [DigitalOutputDevice(pin) for pin in row_pins]
        # Initialize column pins as Buttons
        self.cols = [Button(pin, pull_up=False) for pin in col_pins]
        
    # Return pressed key on keypad
    def keypress(self):
       
        # Scan each row and column to identify pressed key
        for i, row in enumerate(self.rows):
            row.on()  # Enable the current row
            for j, col in enumerate(self.cols):
                if col.is_pressed:  # Check if the column button is pressed
                    # Calculate the key index based on row and column
                    index = i * len(self.cols) + j
                    row.off() # Disable the current row
                    return self.keys[index]
            row.off()


class PhoneBox():
    def __init__(self):
        self.keypad = Keypad(row_pins,col_pins)
        # Initialize LCD
        self.initialize_lcd()
        self.time: int = 0
        self.magnet = picozero.Button(magnetic_switch_pin, pull_up=True)
        self.lock = Servo(Pin(servo_pin))
        
        # Initializes the LCD display
    def initialize_lcd(self):
        i2c = I2C(0, sda=Pin(lcd_sda_pin), scl=Pin(lcd_scl_pin), freq = 400000)
        I2C_ADDR = i2c.scan()[0]
        self.lcd = I2cLcd(i2c, I2C_ADDR, 2, 16) # 2 rows on LCD, 16 columns
        
    def set_timer(self):
        self.lcd.putstr("Enter the desired time in minutes and hit #.")
        keypresses = []
        keypress = self.keypad.keypress()
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
        self.lock.mid()
        self.main_loop()
        
    def main_loop(self):
        self.display_countdown()
        if self.time == 0:
            self.lcd.putstr("Time's up!")
            self.lock.min()
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
                
                
phonebox = PhoneBox()
phonebox.run_phonebox()
        