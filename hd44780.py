#!/usr/bin/python

# modified version of Lance R. Vick's lcd code
# https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py and
# https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp

import RPi.GPIO as GPIO
from time import sleep

class HD44780:
    
    # commands
    LCD_CLEARDISPLAY  = 0x01
    LCD_RETURNHOME    = 0x02
    LCD_ENTRYMODESET  = 0x04
    LCD_DISPLAYCONTROL= 0x08
    LCD_CURSORSHIFT   = 0x10
    LCD_FUNCTIONSET   = 0x20
    LCD_SETCGRAMADDR  = 0x40
    LCD_SETDDRAMADDR  = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    def __init__(self, pin_rs=25, pin_e=24, pins_db=[23, 17, 27, 22]):

        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        self.clear()

    def clear(self):
        """ Blank / Reset LCD """

        self.cmd(0x33) # $33 8-bit mode
        self.cmd(0x32) # $32 8-bit mode
        self.cmd(0x28) # $28 8-bit mode
        self.cmd(0x0C) # $0C 8-bit mode
        self.cmd(0x06) # $06 8-bit mode
        self.cmd(0x01) # $01 8-bit mode

    def cmd(self, bits, char_mode=False):
        """ Send command to LCD """

        sleep(0.001)
        bits=bin(bits)[2:].zfill(8)

        GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i-4], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""

        for char in text:
            if char == '\n':
                self.cmd(0xC0) # next line
            else:
                self.cmd(ord(char),True)

if __name__ == '__main__':

    lcd = HD44780()

    lcd.message(" I'm Raspberry Pi\n  Take a byte!")