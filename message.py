#!/usr/bin/python

from hd44780 import HD44780
from time import sleep, strftime
from subprocess import *
import json

display = HD44780()

ip_addr_cmd = "ip -4 -o addr show %s | cut -d ' ' -f7 | cut -d/ -f1"
status_json = dict()

def execute_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
    
def get_ip(devname):
    ip = execute_cmd(ip_addr_cmd % devname)
    if not ip:
        ip = "Unknown IP"
    return ip

def client_send_message():
    import socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect('/var/run/netconnectd.sock')
    try:
        sock.sendall('{"status":{}}' + '\x00')
        buffer = []
        while True:
            chunk = sock.recv(16)
            if chunk:
                buffer.append(chunk)
                if chunk.endswith('\x00'):
                    break

        data = ''.join(buffer).strip()[:-1]
        json_message = json.loads(data.strip())
        return json_message
    finally:
        sock.close()

def update_display(data):
    display.clear()
    
    display_msg = ""
    ip_wifi = get_ip("wlan0")
    ip_wire = get_ip("eth0")
    
    if (data['result']['connections']['ap']):
        display_msg = "WiFi: MrBeamAP\n%s" % ip_wifi
    elif (data['result']['connections']['wifi']):
        wifiname = data['result']['wifi']['current_ssid']
        display_msg = "WiFi: %s\n%s" % (wifiname, ip_wifi)
    elif (data['result']['connections']['wired']):
        display_msg = "Cable/LAN\n%s" % ip_wire
    else:
        display_msg = "No connection"
    
    display.message(display_msg)


display.clear()
while 1:
    nu_status_json = client_send_message()
    
    if (nu_status_json and nu_status_json != status_json):
        status_json = nu_status_json
        update_display(status_json)
        
    sleep(5)
