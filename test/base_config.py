#!/usr/bin/env python
import yaml
import jinja2
from pprint import pprint
from getpass import getpass

filename = "base_config.yml"
with open(filename) as f:
    initial_config = yaml.full_load(f)


template_file = "base_configa.j2"
with open(template_file) as f:
    config_template = f.read()

initial_config['password'] = getpass()
pprint(initial_config)

template = jinja2.Template(config_template)
print(template.render(initial_config))
