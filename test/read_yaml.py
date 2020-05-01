#!/usr/bin/env python
from pprint import pprint
import yaml

filename = "my_devices.yml"
with open(filename) as f:
    output = yaml.full_load(f)

pprint(output)
print(type(output))
