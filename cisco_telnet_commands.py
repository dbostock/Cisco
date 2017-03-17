import os
import telnetlib
import errno
import socket

path="C:\python\list.txt"
with open(path, 'r') as f:
	for host in f:
		HOSTN = host.rstrip()
		print "scanning " + (HOSTN) + " ..."
#Enter username here
		user  = ""
#Enter password here
		password = ""
#Catch Timeouts
		try:
#Telnet into the host
			telnet  = telnetlib.Telnet(HOSTN, 23, timeout=15)
			telnet.read_until('Username: ', 3)
			telnet.write(user + '\r')
			telnet.read_until('Password: ', 3)
			telnet.write(password + '\r')
# telnet.write('enable' + '\r\n')
# telnet.write('enable_password' + '\r\n')
			telnet.write('term len 0' + '\r\n')
#Cisco commands to be run
			telnet.write('sh run | i hostname' + '\r\n')
			telnet.write('sh mod | i Unknown' + '\r\n')
			telnet.write('exit' + '\r')
			a=telnet.read_all() 
			f = open("test2"+".txt", 'w')
			f.write(str(a))
			print "Host " + (HOSTN) + " information written to " + path
#Catch Timeout error, print messages
		except socket.timeout:
			print "Timeout for host " + (HOSTN) + " ...\n"
		except socket.error:
			print "Connection Refused " + (HOSTN) + " ...\n"
			pass
			print "Scanning Complete"
