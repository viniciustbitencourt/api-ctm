#!/usr/bin/python2.7

import telnetlib

HOST="10.128.164.1"
PORTA="8443"
tn = telnetlib.Telnet(HOST, PORTA)

print (tn)