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
'''
from netmiko import ConnectHandler
from getpass import getpass
import re
import pdb

def file_template():
    f = open("tunnel_template.txt", mode="w")
    f.write("tunnel_type:gre|ipsec\n")
    f.write("username:admin\n")
    f.write("device1:172.16.1.1\n")
    f.write("device1_type:cisco_ios\n")
    f.write("device1_tunnel_ip:10.254.254.1 255.255.255.252\n")
    f.write("device1_subnet:10.1.1.0 255.255.255.0\n")
    f.write("device2:172.16.1.5\n")
    f.write("device2_type:cisco_ios\n")
    f.write("device2_tunnel_ip:10.254.254.2 255.255.255.252\n")
    f.write("device2_subnet:10.5.5.0 255.255.255.0\n")
    f.close()

    print("File does not exist, file 'tunnel_template.txt' created...")
    return

def build_parameters():
#build dictionary of input parameters
    for line in output:
        if re.search(r"^.", line) != "#":
            i = re.search(r"(^.*):(.*)", line)
            inputs[i.group(1)] = i.group(2)

def tunnel_gre():
#build device login profiles
    password = getpass()

    dev1  = {'ip'          : inputs['device1'],
             'device_type' : inputs['device1_type'],
             'username'    : inputs['username'],
             'password'    : password
              }

    dev2  = {'ip'          : inputs['device2'],
             'device_type' : inputs['device2_type'],
             'username'    : inputs['username'],
             'password'    : password
              }

#    pdb.set_trace()
    connection = ConnectHandler(**dev1)
    print("Building 'A' end....")

    cmd = ['interface tunnel0',
           'ip address ' + inputs['device1_tunnel_ip'],
           'tunnel source ' + inputs['device1'],
           'tunnel destination ' + inputs['device2'],
           'ip route ' + inputs['device2_subnet'] + ' tunnel0']
    result = connection.send_config_set(cmd)
    print("-" * 80)
    print(result)
    print("-" * 80)

    connection.disconnect()
    print("'A' end complete")

    connection = ConnectHandler(**dev2)
    print("Building 'B' end....")

    cmd = ['interface tunnel0',
           'ip address ' + inputs['device2_tunnel_ip'],
           'tunnel source ' + inputs['device2'],
           'tunnel destination ' + inputs['device1'],
           'ip route ' + inputs['device1_subnet'] + ' tunnel0']
    result = connection.send_config_set(cmd)
    print("-" * 80)
    print(result)
    print("-" * 80)

    connection.disconnect()
    print("'B' end complete")

def tunnel_ipsec():
    return


#get tunnel and device info
try:
    with open("tunnel.txt") as infile:
        output = infile.read().splitlines()
        inputs = {}
        build_parameters()
    if inputs['tunnel_type'] == 'gre':
        tunnel_gre()
    elif inputs['tunnel_type'] == 'ipsec':
        tunnel_ipsec()
    else:
        print("Invalid tunnel type, must be 'gre' or 'ipsec'")
        exit()

    print('''\n\nTunnel build complete, please test connectivity then save config\n
        on DevA and DevB''')

except FileNotFoundError:
    file_template()
