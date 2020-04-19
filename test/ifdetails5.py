#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass

passwd = getpass()

interfaces = open("interface_status.txt", "w")

#open list of known devices
with open("devices.txt") as infile:
  for line in infile:
    name,ipaddr = line.rstrip().split(',')
#for each ip address in devices.txt, connect and pull interface list
# split into a list of stings exluding the header row
    connection = ConnectHandler(ip=ipaddr, device_type="cisco_ios", username="admin", password=passwd)
    output = connection.send_command("sh int status")
    iflist = output.split("\n")
    iflist.pop(0)
#for each interface string in the table add hostname and ip and
# adjust the sting to be comma separated values
    for i in range (len(iflist)):
        iflist[i] = ",".join(iflist[i].split())
        iflist[i] = name + "," + ipaddr + "," + iflist[i] + "\n"
        interfaces.write(iflist[i])
    connection.disconnect()

infile.close()
interfaces.close()
