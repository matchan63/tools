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
dom = "." + connection.send_command("show ip domain-name")
#initial list population
#local / first device (nominated by user above in "device")
device_list.append([local_device[0]['hostname']+dom,device])
working_list.append(local_device[0]['hostname']+dom)
#disconnect
connection.disconnect()

#begin trace of devices using CDP neighbors found on gateway device
for dev in device_list:
    print("\n",dev[1],"\n")
    connection = ConnectHandler(ip=dev[1], device_type="cisco_ios", username="admin", password=passwd)
    cdp_devices = connection.send_command("show cdp neighbors detail", use_textfsm=True)
    connection.disconnect()
    for neighbor in cdp_devices:
        if neighbor['destination_host'] not in working_list:
            device_list.append([neighbor['destination_host'],neighbor['management_ip']])
            working_list.append(neighbor['destination_host'])

with open("devices.txt", "w") as f:
    for dev in device_list:
        line = dev[0] + "," + dev[1] + "\n"
        f.write(line)

f.close()
