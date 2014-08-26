#!/usr/bin/python

from hd44780 import HD44780
from subprocess import *
from time import sleep, strftime

display = HD44780()

ip_addr_cmd = "ip -4 -o addr show wlan0 | cut -d ' ' -f7 | cut -d/ -f1"

def execute_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output


while 1:
    display.clear()
    ipv4 = execute_cmd(ip_addr_cmd)
    display.message(" Mr Beam \n"+ipv4)
    sleep(10)