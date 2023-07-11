#!/usr/bin/python3
#
# panos_cmd.py
# Opengear Solution Engineering, 18 Jan 2021
#
# SLE-149
# Send a command to a Palo-Alto device via pmshell

from __future__ import unicode_literals, print_function
import time
from netmiko import ConnectHandler, redispatch

net_connect = ConnectHandler(
    device_type='terminal_server',        # Notice 'terminal_server' here
    ip='10.10.10.102', 
    username='root+port08', 
    password='default')

# Manually handle interaction in the Terminal Server 
# (fictional example, but hopefully you see the pattern)
# Send Enter a Couple of Times
net_connect.write_channel("\r\n")
time.sleep(1)
net_connect.write_channel("\r\n")
time.sleep(1)
output = net_connect.read_channel()
print(output)                             # Should hopefully see the terminal server prompt

# Login to end device from terminal server
#net_connect.write_channel("connect 1\r\n")
#time.sleep(1)

# Manually handle the Username and Password
max_loops = 3
i = 1
while i <= max_loops:
    output = net_connect.read_channel()
    
    if 'login' in output:
        net_connect.write_channel('admin\r\n')
        time.sleep(1)
        output = net_connect.read_channel()

    # Search for password pattern / send password
    if 'Password' in output:
        net_connect.write_channel('admin\r\n')
        time.sleep(1)
        output = net_connect.read_channel()
    if 'old' in output:
        net_connect.write_channel('admin\r\n')
        time.sleep(1)
        output = net_connect.read_channel()
    if 'new' in output:
        net_connect.write_channel('C0mplexity!\r\n')
        time.sleep(1)
        output = net_connect.read_channel()
    if 'Confirm' in output:        
        net_connect.write_channel('C0mplexity!\r\n')
        time.sleep(1)
        output = net_connect.read_channel()
    # Did we successfully login
        if '>' in output or '#' in output:
            break
    net_connect.write_channel('\r\n')
    time.sleep(.5)
    i += 1

# We are now logged into the end device  

# Dynamically reset the class back to the proper Netmiko class
redispatch(net_connect, device_type='paloalto_panos')

# Deploy a set of commands to bootstrap the PA Device.

commands = ['set deviceconfig system ip-address 10.10.10.210', 
            'set deviceconfig system netmask 255.255.255.0', 
            'set deviceconfig system hostname pa-test-device',
            'set deviceconfig system default-gateway 10.10.10.10',
            'set deviceconfig system dns-setting servers primary 10.10.10.50',
            'set deviceconfig system dns-setting servers secondary 10.10.10.51',
            'set deviceconfig system panorama-server 10.10.10.50',
            'set deviceconfig system panorama-server-2 10.10.10.51',
            'commit'
]
net_connect.send_command("configure", expect_string=r"#", strip_prompt=False, strip_command=False)
output = net_connect.send_config_set(commands)
print(output)

net_connect.disconnect()