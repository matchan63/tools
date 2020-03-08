from netmiko import ConnectHandler 
from getpass import getpass

#I added a comment
connection = ConnectHandler(ip="10.1.1.251", device_type="cisco_ios", username="admin", password=getpass())

#added another comment to check changes in git
print (connection.send_command("sh ip int brief | ex una"))

#another comment to check changes in git
connection.disconnect()
