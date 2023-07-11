#!/usr/bin/python3
#
# cisco_cmd.py
# Opengear Solutions Engineering, 8 Feb 2022
#  
# SLE-157
# Send a command to a Cisco IOS device through OM pmshell
# Validated on IOS XE version 16.12.04 and IOS version 15.2(7)E4

from netmiko import ConnectHandler, redispatch
import getpass
import time

def connect():

    device1 = {
        'host': '10.0.0.4', #change to OM's IP
        'username': 'root',
        'password': 'Op3ng3ar!',
        'device_type': 'terminal_server',
        'session_log': 'netmiko_log.txt'
    }   

    conn = ConnectHandler(**device1)

    return conn


def command():

    conn = connect()

    conn.send_command_timing('pmshell -l /dev/port21')
    conn.write_channel('\r\n\r\n\r\n')
    time.sleep(5)
    conn.write_channel('\r\n\r\n')

    redispatch(conn, device_type='cisco_ios')
    conn.find_prompt()

    conn.enable()  
    output = conn.send_command('show ip interface brief')
    print(output)

    conn.write_channel('\r\n')
    time.sleep(1)

    conn.disconnect()


if __name__ == "__main__":
    command()