#!/usr/bin/env python
#
# Assumptions:
'''
1. username and password is the same for both devices
2. Tunnel0 is not in use!!!
3. Device IP will be used as tunnel source and destination
'''

# To Do's
'''
1. Test if tunnel number already in use
2. All error checking, ip, mask, etc
3. Differentiate between management address of device and tunnel interface,
    perhaps ask for interface name and reverse engieneer the IP, could also
    validate interface is usable...
4. accept tunnel number, overwrite if exists, if blank choose next available
5. accept input from a file instead (next version)
    build template file if no input file exists
'''
from netmiko import ConnectHandler
from getpass import getpass

dev1  = {'ip'          : '',
         'device_type' : 'cisco_ios',
         'username'    : 'admin',
         'password'    : ''
          }

dev2  = {'ip'          : '',
         'device_type' : 'cisco_ios',
         'username'    : 'admin',
         'password'    : ''
          }

dev1['ip'] = input("IP address or FQDN for device1 (tunnel 'A' end): ")
tunnel_a_addr = input("IP address of 'A' end tunnel interface: ")
tunnel_a_subnet = input("Subnet and mask of 'A' end tunnel interface: ")
dev2['ip'] = input("IP address or FQDN for device2 (tunnel 'B' end): ")
tunnel_b_addr = input("IP address of 'B' end tunnel interface: ")
tunnel_b_subnet = input("Subnet and mask of 'B' end tunnel interface: ")

dev1['password'] = getpass()
dev2['password'] = dev1['password']

connection = ConnectHandler(**dev1)
print("Building 'A' end....")

cmd = ['interface tunnel0',
       'ip address ' + tunnel_a_addr + ' 255.255.255.0',
       'tunnel source ' + dev1['ip'],
       'tunnel destination ' + dev2['ip'], 'exit',
       'ip route ' + tunnel_b_subnet + ' tunnel0']
output = connection.send_config_set(cmd)
print("-" * 80)
print(output)
print("-" * 80)

connection.disconnect()
print("'A' end complete")

connection = ConnectHandler(**dev2)
print("Building 'B' end....")

cmd = ['interface tunnel0',
       'ip address ' + tunnel_b_addr + ' 255.255.255.0',
       'tunnel source ' + dev2['ip'],
       'tunnel destination ' + dev1['ip'], 'exit',
       'ip route ' + tunnel_a_subnet + ' tunnel0']
output = connection.send_config_set(cmd)
print("-" * 80)
print(output)
print("-" * 80)

connection.disconnect()
print("'B' end complete")

print('''\n\nTunnel build complete, please test connectivity then save config\n
        on DevA and DevB''')
