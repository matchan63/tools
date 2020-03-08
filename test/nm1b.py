from netmiko import ConnectHandler 
from getpass import getpass

connection = ConnectHandler(ip="10.1.1.251", device_type="cisco_ios", username="admin", password=getpass())

print (connection.send_command("sh ip int brief | ex una"))

connection.disconnect()
