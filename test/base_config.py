#!/usr/bin/env python
import yaml
import jinja2
from pprint import pprint

filename = "base_config.yml"
with open(filename) as f:
    active_interfaces = yaml.full_load(f)


template_file = "base_config.j2"
with open(template_file) as f:
    interface_template = f.read()

print("active_interfaces")
pprint(active_interfaces)
print("\nactive_interfaces['interfaces']")
pprint(active_interfaces['interfaces'])

template = jinja2.Template(interface_template)
print(template.render(active_interfaces = active_interfaces['interfaces']))
