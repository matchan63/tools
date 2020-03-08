from netmiko import ConnectHandler 
from getpass import getpass

#add a comment:
connection = ConnectHandler(ip="10.1.1.251", device_type="cisco_ios", username="admin", password=getpass())

#adding further comments to test git
print (connection.send_command("sh ip int brief | ex una"))

connection.disconnect()
