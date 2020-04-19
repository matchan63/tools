#!/usr/bin/env python
from netmiko import ConnectHandler 
from getpass import getpass

device_list = {}
passwd = getpass()

with open("devices.txt") as infile:
  for line in infile:
    print(line)
    name,ipaddr = line.rstrip().split(',')
    device_list[name] = ipaddr

for name in device_list:
 print(device_list[name])

for name in device_list:
  print("%s" % (device_list[name]))
  connection = ConnectHandler(ip=device_list[name], device_type="cisco_ios", username="admin", password=passwd)
  print (connection.send_command("sh ip int brief | ex una"))
  print ("\n")
  connection.disconnect()

