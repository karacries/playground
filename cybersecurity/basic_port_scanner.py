'''
Very basic port scanner, lacks cross-platform support (only utilizes macOS and MAYBE linux commands)
'''
import os
import platform
import socket
from concurrent.futures import ThreadPoolExecutor
from scapy.all import *
from datetime import datetime
import subprocess, re
from impacket.nmb import *
import sqlite3, time
from contextlib import closing

def get_network_ip_range():
    """Get the base IP range from the local machine's IP."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Your local IP: {local_ip}")

    # Assuming /24 subnet (e.g., 192.168.1.0/24)
    ip_base = ".".join(local_ip.split('.')[:-1]) + "."
    return ip_base

def ping_ip(ip):
    """Ping a given IP and return whether it is alive."""
    # Adjust ping command depending on the operating system
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    command = f"ping {param} -w 1 {ip} >nul 2>&1" if platform.system().lower() == "windows" else f"ping {param} -W 1 {ip} >/dev/null 2>&1"
    
    # Run the command and return True if ping was successful
    return os.system(command) == 0

def scan_network(ip_base):
    """Scan the entire /24 subnet of the local IP."""
    print(f"Scanning network: {ip_base}0/24")

    live_hosts = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        # Schedule ping tasks for all IPs in the subnet
        futures = {executor.submit(ping_ip, f"{ip_base}{i}"): i for i in range(1, 255)}
        
        # Collect the results as they complete
        for future in futures:
            ip = f"{ip_base}{futures[future]}"
            if future.result():
                live_hosts.append(ip)

    return live_hosts

def display_hosts(hosts):
    """Display the found live hosts."""
    if hosts:
        print(f"\nFound {len(hosts)} live host(s) on the network:")
        for i, ip in enumerate(hosts, start=1):
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                hostname = "Unknown Host"
            print(f"{i}. IP: {ip}, Hostname: {hostname}")
    else:
        print("No hosts found.")

def arp_cache_map():
    """we looking 4 mac addresses"""
    out = subprocess.check_output(["arp", "-a"], text=True, errors="ignore") # run arp -a in the terminal to return mac addresses
    ip_mac = {} # empty dictionary to store those addresses
    for line in out.splitlines(): # go thru the output line by line
        m = re.search(r"\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-f:\-]+)", line, re.I) # look for an IP inside (), one or more digits, dots, grab mac address like strings, re.I makes it case insensitive
        if m: # if it matches
            ip, mac = m.group(1), m.group(2).replace("-", ":") # turns the dashes to colons, group 1 is ip and group 2 is mac
            ip_mac[ip] = mac # put it in the dictionary
    return ip_mac


if __name__ == "__main__":
    ip_base = get_network_ip_range()
    live_hosts = scan_network(ip_base)
    display_hosts(live_hosts)
    ip_mac = arp_cache_map()
    print("\nResults:")
    for ip in live_hosts: # for everything connected to the network that was found before,
        mac = ip_mac.get(ip) # show the mac addresses
        print(f"MAC: {(mac or "x"):>17}")

