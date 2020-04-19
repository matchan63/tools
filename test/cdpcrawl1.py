#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint
# Assumptions, standardised passwords / security
# Starting point will be the local gateway, requested from username
# will only find device branches as routes allow

device_list = []
working_list = []
passwd = getpass()
device = input("local gateway address: ")
#Connect to first device
connection = ConnectHandler(ip=device, device_type="cisco_ios", username="admin", password=passwd)
#Get local and cdp connected device info
local_device = connection.send_command("show version", use_textfsm=True)
cdp_devices = connection.send_command("show cdp neighbors detail", use_textfsm=True)

#initial list population
#local / first device (nominated by user above in "device")
device_list.append([local_device[0]['hostname'],local_device[0]['hardware'][0],device])
#first CDP neighbors found
for dev in cdp_devices:
    device_list.append([dev['destination_host'],dev['platform'],dev['management_ip']])
    working_list.append([dev['destination_host'],dev['platform'],dev['management_ip']])
pprint(device_list)
#disconnect
connection.disconnect()

#begin trace of devices using CDP neighbors found on gateway device
#for dev in working_list:
#    connection = ConnectHandler(ip=dev[2], device_type="cisco_ios", username="admin", password=passwd)
#    cdp_devices = connection.send_command("show cdp neighbors detail", use_textfsm=True)
#    working_list.append([dev['destination_host'],dev['platform'],dev['management_ip']])
#    connection.disconnect()

#with open("devices.txt") as infile:
#  for line in infile:
#    print(line)
#    name,ipaddr = line.rstrip().split(',')
#    device_list[name] = ipaddr
