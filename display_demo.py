#!/usr/bin/python

from hd44780 import HD44780
from subprocess import *
from time import sleep

display = HD44780()

lines = [
"Mr Beam ,       ",
"an open source  ",
"DIY laser cutter"
"and engraver kit",
"                ",
"Follow us:      ",
"blog.mr-beam.org",
"@MrBeamLasers   ",
"                ",
"Mr Beam cuts    ",
"paper           ",
"thin cardboard  ",
"fabric & felt   ",
"thin leather    ",
"foam rubber     ",
"foam board      ",
"foil (stickers!)",
"kraftplex       ",
"thin light wood ",
"latex           ",
"                ",
"Mr Beam engraves",
"almost every    ",
"surface like    ",
"wood & leather  ",
"chocolate       ",
"steaks          ",
"plastic         ",
"velvet          ",
"and many more   ",
"                ",
"Visit           ",
"www.mr-beam.org ",
"for details.    ",
"                "
]

l = len(lines)

display.clear()
start = 0
while 1:
    line0 = lines[(start + l-1) % l]
    line1 = lines[start]
    line2 = lines[(start+1) % l]
    for i in range(1,18):
        _line1 = (line1[0:i-1]+' ' + line0[i:])[0:16]
        _line2 = (line2[0:i-1]+' ' + line1[i:])[0:16]
        #display.clear()
        sleep(0.0001)
        display.message(_line1 + "\n" + _line2)
        sleep(0.005)
    display.message(_line1+"\n" + _line2)
    start = (start + 1) % l 
    sleep(2)


