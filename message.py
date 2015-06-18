#!/usr/bin/python

from hd44780 import HD44780
from time import sleep
from subprocess import *
import json
import socket


display = HD44780()

ip_addr_cmd = "ip -4 -o addr show %s | cut -d ' ' -f7 | cut -d/ -f1"
port5000_cmd = "netstat -tln | grep :5000"
text = [""]
current_text = ""


def execute_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output
	
def get_ip(devname):
	ip = execute_cmd(ip_addr_cmd % devname)
	if not ip:
		ip = "Unknown IP"
	return ip

def octoprint_running():
	netstat_out = execute_cmd(port5000_cmd)
	if("0.0.0.0:5000" in netstat_out):
		return True
	else:
		return False

def request_status_from_socket():
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	try:
		sock.connect('/var/run/netconnectd.sock')
		sock.sendall('{"status":{}}' + '\x00')
		buffer = []
		while True:
			chunk = sock.recv(16)
			if chunk:
				buffer.append(chunk)
				if chunk.endswith('\x00'):
					break

		json_string = ''.join(buffer).strip()[:-1]
		data = json.loads(json_string.strip())
		return data

	except socket.error, exc:
		#print("socket not ready", exc);
		return None
	finally:
		sock.close()

def get_text(data):
	display_msg = ""
	if(data != None and 'result' in data and 'connections' in data['result']):
		conn = data['result']['connections']
		if ('ap' in conn and conn['ap'] == True):
			ip_wifi = get_ip("wlan0")
			display_msg = "WiFi: MrBeamAP\n%s" % ip_wifi
		elif ('wired' in conn and conn['wired'] == True):
			ip_wire = get_ip("eth0")
			display_msg = "Cable/LAN\n%s" % ip_wire
		elif ('wifi' in conn and conn['wifi'] == True):
			ip_wifi = get_ip("wlan0")
			wifiname = data['result']['wifi']['current_ssid']
			display_msg = "WiFi: %s\n%s" % (wifiname, ip_wifi)
	else:
		display_msg = "No connection"
	return display_msg
	
def update_display(msg):
	display.clear()
	sleep(0.3)
	display.message(msg)


display.clear()
i = 0
while 1:
	new_status = request_status_from_socket()
	text = [get_text(new_status)]
	if(not octoprint_running()):
		text.append("waiting...\n\n")

	
	i = (i+1) % len(text)
	new_text = text[i]
	if (new_text != current_text):
		current_text = new_text
		update_display(current_text)	
	sleep(2)
