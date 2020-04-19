#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass

device_list = {}
passwd = getpass()

with open("devices.txt") as infile:
  for line in infile:
    name,ipaddr = line.rstrip().split(',')
    device_list[name] = ipaddr

outputl = []

interfaces = open("interfaces.txt", "w")
for name in device_list:
#  print("%s" % (device_list[name]))
  connection = ConnectHandler(ip=device_list[name], device_type="cisco_ios", username="admin", password=passwd)
  output = connection.send_command("sh ip int brief | ex una")
  iflist = output.split("\n")
  iflist.pop(0)
  for i in range (len(iflist)):
    iflist[i] = ",".join(iflist[i].split())
    iflist[i] = device_list[name] + "," + iflist[i] + "\n"
    interfaces.write(iflist[i])
  outputl = outputl + iflist
  connection.disconnect()

infile.close()
interfaces.close()
print(outputl)
