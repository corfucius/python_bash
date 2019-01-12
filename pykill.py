#!/usr/bin/env python3

'''
    -------------------------------------------------------------------
    A script to kill processes that may interfere with running aircrack
    -------------------------------------------------------------------
    by: corfucius
'''
import optparse
import subprocess

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-w", "--wirelss", dest="wireless", help="Enter the name of your wireless card, ex: wlan0, wlp0s, etc.. Use -w or --wireless")
    (options, arguments) = parser.parse_args()
    if not options.wireless:
        parser.error("[-] Please enter the name of your wireless card, An example: -w wlan0, or --wireless wlp0s")
    return options



def get_processes(wireless):
    '''
        Create an object full of troublesome processes
    '''
    process = subprocess.run(["sudo", "airmon-ng", "check", wireless],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    check=True,
    text=True)
    return process.stdout

def kill_processes(processes):
    '''
        1. Create parsed list from object
        2. Iterate through list and remove any numbers in object that are less than 4 digits.
        3. Kill processes
    '''
    print(processes)
    proc_list = [int(s) for s in processes.split() if s.isdigit()]
    for item in proc_list:
        if len(str(item)) < 3:
            proc_list.remove(item)
    print("Your list of current process to kill is: ", proc_list)
    for item in proc_list:
        p = str(item)
        subprocess.run(["sudo", "kill", p])
        print(p, " is dead now")

options = get_arguments()
processes = get_processes(options.wireless)
kill_processes(processes)
