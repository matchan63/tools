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
import re
import pdb

def file_template():
    return

def tunnel_gre():
#build device login profiles
    password = getpass()

    dev1  = {'ip'          : re.search(r"^.*:(.*)", output[2]).group(1),
             'device_type' : re.search(r"^.*:(.*)", output[3]).group(1),
             'username'    : re.search(r"^.*:(.*)", output[1]).group(1),
             'password'    : password
              }

    dev2  = {'ip'          : re.search(r"^.*:(.*)", output[6]).group(1),
             'device_type' : re.search(r"^.*:(.*)", output[7]).group(1),
             'username'    : re.search(r"^.*:(.*)", output[1]).group(1),
             'password'    : password
              }

#    pdb.set_trace()
    connection = ConnectHandler(**dev1)
    print("Building 'A' end....")

    cmd = ['interface tunnel0',
           'ip address ' + re.search(r"^.*:(.*)", output[4]).group(1),
           'tunnel source ' + re.search(r"^.*:(.*)", output[2]).group(1),
           'tunnel destination ' + re.search(r"^.*:(.*)", output[6]).group(1),
           'ip route ' + re.search(r"^.*:(.*)", output[9]).group(1) + ' tunnel0']
    result = connection.send_config_set(cmd)
    print("-" * 80)
    print(result)
    print("-" * 80)

    connection.disconnect()
    print("'A' end complete")

    connection = ConnectHandler(**dev2)
    print("Building 'B' end....")

    cmd = ['interface tunnel0',
           'ip address ' + re.search(r"^.*:(.*)", output[8]).group(1),
           'tunnel source ' + re.search(r"^.*:(.*)", output[6]).group(1),
           'tunnel destination ' + re.search(r"^.*:(.*)", output[2]).group(1),
           'ip route ' + re.search(r"^.*:(.*)", output[5]).group(1) + ' tunnel0']
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
    if 'tunnel_type:gre' in output:
        tunnel_gre()
    elif 'tunnel_type:ipsec' in output:
        tunnel_ipsec()
    else:
        print("Invalid tunnel type, must be 'gre' or 'ipsec'")
        exit()

    print('''\n\nTunnel build complete, please test connectivity then save config\n
        on DevA and DevB''')

except FileNotFoundError:
    print("File does not exist, template file created...")
    exit()
