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

# Import all the necessary libraries
from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
from picozero import Button, Servo, DigitalOutputDevice
import time

# Pins and lists of pins that were used to initialize the project
lcd_sda_pin = 12 
lcd_scl_pin = 13 
row_pins = [26, 22, 21, 20] 
col_pins = [19, 18, 17, 16]
magnetic_switch_pin = 0 # Subject to change
servo_pin = 2

# Keypad class that stores all the properties and methods relevant to the keypad
class Keypad():
    # Initialize Keypad object
    def __init__(self, row_pins, col_pins):
        self.keys = ["1", "2", "3", "A",
                     "4", "5", "6", "B",
                     "7", "8", "9", "C",
                     "*", "0", "#", "D"]
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
                    print(self.keys[index])
                    time.sleep(0.25)
                    return self.keys[index]
            row.off()

# TO DO: Magnetic reed switch, how to improve message, keep track of pauses

# Main class that contains everything to run the project
class PhoneBox():
    # Initialize PhoneBox object
    def __init__(self):
        # Create keypad
        self.keypad = Keypad(row_pins,col_pins)
        # Initialize LCD
        self.initialize_lcd()
        # Set time to 0
        self.time: int = 0
        # Initialize magnetic reed switch
        self.magnet = Button(magnetic_switch_pin, pull_up=True)
        # Initialize servo to lock prize compartment
        self.lock = Servo(servo_pin)
        
    # Initializes the LCD display
    def initialize_lcd(self):
        i2c = I2C(0, sda=Pin(lcd_sda_pin), scl=Pin(lcd_scl_pin), freq = 400000)
        I2C_ADDR = i2c.scan()[0]
        self.lcd = I2cLcd(i2c, I2C_ADDR, 2, 16) # 2 rows on LCD, 16 columns
        
    # Sets timer based on user input
    def set_timer(self):
        self.lcd.putstr("Enter time in")
        self.lcd.move_to(0,1)
        self.lcd.putstr("min and hit #")
        keypresses = ""
        keypress = self.keypad.keypress()
        while keypress != "#":
            if keypress != None:
                keypresses += keypress
                print(keypress)
                self.lcd.clear()
                self.lcd.putstr(keypresses)
            keypress = self.keypad.keypress()
        
        self.time = int(keypresses)*60
        self.lcd.clear()
        print(self.time)
            
    # Displays countdown
    def display_countdown(self):
        while self.time != 0 and self.keypad.keypress() != "#":
            self.lcd.putstr(self.time_display_format())
            time.sleep(1)
            self.time -= 1
            self.lcd.clear()
            
    # Returns time in minute:second format
    def time_display_format(self):
        min = int(self.time/60)
        sec = self.time - min*60
        return f"{min}:{sec}"
    
    # Main function to run phonebox
    def run_phonebox(self):
        self.set_timer()
        self.lock.mid()
        self.main_loop()
        
    # Main loop of the phonebox
    def main_loop(self):
        self.lcd.clear()
        self.display_countdown()
        if self.time == 0:
            self.lcd.putstr("Time's up!")
            self.lock.min()
        else:
            self.lcd.putstr("Why did you stop")
            time.sleep(1)
            self.lcd.clear()
            pause_options = {"A": "A:Vital message", "B": "B:I give up"}
            display_string = pause_options["A"]
            while (keypress := self.keypad.keypress()) not in pause_options.keys():
                self.lcd.putstr("Why did you stop")
                self.lcd.move_to(0,1)
                self.lcd.putstr(display_string)
                display_string = pause_options["A"] if display_string != pause_options["A"] else pause_options["B"]
                time.sleep(1)
                self.lcd.clear()
            print("Keypress", keypress)
            if keypress == "A":
                print('hi')
                self.lcd.putstr("Vital message")
            elif keypress == "B":
                self.lcd.putstr("You gave up")
            self.lcd.move_to(0,1)
            self.lcd.putstr("Hit # to resume")
            while keypress := self.keypad.keypress() != "#":
                pass
            self.main_loop()
                
                
phonebox = PhoneBox()
print(phonebox.keypad.keypress())
phonebox.run_phonebox()
        