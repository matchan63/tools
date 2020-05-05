#!/usr/bin/env python
from netmiko import Netmiko
import yaml
import jinja2
from pprint import pprint
from getpass import getpass

login = {'ip'          : '10.1.1.251',
         'device_type' : 'cisco_ios',
         'username'    : 'admin',
         'password'    : 'cisco'
          }

filename = "base_config.yml"
with open(filename) as f:
    initial_config = yaml.full_load(f)


template_file = "base_configb.j2"
with open(template_file) as f:
    config_template = f.read()

initial_config['password'] = getpass()

template = jinja2.Template(config_template)
cmd = template.render(initial_config).splitlines()

f = open("commands.txt", "w")
cmd=map(lambda x:x+'\n', cmd)
f.writelines(cmd)
f.close()

connection = Netmiko(**login)
output = connection.send_config_from_file("commands.txt")
print(output)
connection.disconnect()
