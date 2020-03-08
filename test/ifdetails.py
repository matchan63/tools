from netmiko import ConnectHandler 
from getpass import getpass

device_list = {}

connection = ConnectHandler(ip="10.1.1.251", device_type="cisco_ios", username="admin", password=getpass())

with open("devices.txt") as infile:
  for line in infile:
    print(line)
    name,ipaddr = line.rstrip().split(',')
    if name in device_list:
      device_list[name].append(ipaddr)
    else:
      device_list[name] = [ipaddr]

print(device_list)

#print (connection.send_command("sh ip int brief | ex una"))

connection.disconnect()
