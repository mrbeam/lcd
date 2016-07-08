#!/usr/bin/python

from hd44780 import HD44780
from time import sleep
import json
import socket
import netifaces

interfaces = netifaces.interfaces()
display = HD44780()
current_text = ""

def octoprint_running():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = s.connect_ex(('127.0.0.1',5000))
	s.close()
	if result == 0:
		return True
	else:
		return False

def get_ip_by_interface(ifname):
	ipInfo = netifaces.ifaddresses(ifname)
	try:
		return ipInfo[netifaces.AF_INET][-1]['addr']
	except:
		return False

def request_status_from_socket():
	socket.setdefaulttimeout(1)
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
		return False
	finally:
		sock.close()

def update_display(msg):
	global current_text
	if (current_text != msg):
		current_text = msg
		display.clear()
		sleep(0.3)
		display.message(msg)
	sleep(7)

display.clear()
i = 0
while 1:
	if(not octoprint_running()):
		update_display('Starting MrBeam\nInterface...')
	else:
		update_display('MrBeam ready!')	
	for (interface, name) in enumerate(interfaces):
		if (name == 'eth0' and get_ip_by_interface(name)):
			update_display("Interface: %s\n%s" % (name, get_ip_by_interface(name)))
		if (name == 'wlan0' and get_ip_by_interface(name)):
			data = request_status_from_socket()
			if data:
				conn = data['result']['connections']
				if ('ap' in conn and conn['ap'] == True):
					update_display("WIFI: MrBeamAP\n%s" % get_ip_by_interface(name))
				elif ('wifi' in conn):
					wifiname = data['result']['wifi']['current_ssid']
					update_display("WIFI: %s\n%s" % (wifiname, get_ip_by_interface(name)))
