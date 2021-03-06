# Python_Scripts

![alt text](https://github.com/Hitman007IN/Python_Scripts/blob/master/python_logo.jpeg)

# MAC Changer  

Change MAC (Media Access Control) of ethernet chipset (eth0):-
MAC is unique to a device chipset
To change MAC of eth0 (wired network to which virtual images are connected, which actually is the network adapter of original system on which virtual image is hosted) in kali linux
2 ways:-
Terminal 
ifconfig eth0 down
ifconfig eth0 hw ether 00:11:22:33:44:55
ifconfig eth0 up

Python program
subprocess is the module used to run system level commands
Subprocess module contains a number of functions
Commands depends on the OS which executes the script
Syntax
Import subprocess
subprocess.call(“Command_To_Execute”, shell=True)  //call method works on the foreground and doesnt move to next command until the current commands is completed
Or
subprocess.call([“command”,”to”,”execute”])

Example:-
#! usr/local/env python
import subprocess

interface = input("interface > ")
mac_addrss = input("new mac_addr > ")

print("[+] Changing mac address for "+interface+" to "+mac_addrss)

subprocess.call("ifconfig "+interface+" down", shell=True)
subprocess.call("ifconfig "+interface+" hw ether "+mac_addrss, shell=True)
subprocess.call("ifconfig "+interface+" up", shell=True)

input() in Python3 and raw_input in Python2 to get user input from terminal https://docs.python.org/2/library/functions.html#raw_input

optparse is a module that is used to take command line arguments
subprocess.check_output(["ifconfig", interface]) - this will give back the actual command results


#######################################################################################

# Network Scanner
To scan all the devices connected to the same network can be done by, In terminal
Netdiscover -r 10.0.2.1/24 (this is the subnet range instead of specifying the entire ip address range from 10.0.2.1 to 10.0.2.254)

To scan a network there are some steps involved:-
source/attacker machine sends an ARP request packet with the ip address of target machine in the same network
This request is then send as a broadcast packet to all the machines in that network
Once its received, machine with the request ip address responds back with a ARP response packet containing the MAC address

#! /usr/local/env python

import scapy.all as scapy  #Scapy is a packet manipulation tool for networks, written in Python

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)  #creates a ARP packet with the request ip
    print(arp_request.summary())    #ARP who has Net('10.0.2.1/24') says 10.0.2.15
    
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  #create broadcast mac
    print(broadcast.summary())       #08:00:27:74:17:d4 > ff:ff:ff:ff:ff:ff (0x9000)

    arp_request_broadcast = broadcast/arp_request   #combining both
    answered, unanswered = scapy.srp(arp_request_broadcast, timeout=1) #srp is the scapy send or receive packet which returns back 2 list answered (contains packets sent and answered) and unanswered
    print(answered.summary()) 

scan("10.0.2.1/24")

Output
Received 3 packets, got 3 answers, remaining 253 packets
Ether / ARP who has 10.0.2.1 says 10.0.2.15 ==> Ether / ARP is at 52:54:00:12:35:00 says 10.0.2.1 / Padding
Ether / ARP who has 10.0.2.2 says 10.0.2.15 ==> Ether / ARP is at 52:54:00:12:35:00 says 10.0.2.2 / Padding
Ether / ARP who has 10.0.2.3 says 10.0.2.15 ==> Ether / ARP is at 08:00:27:c3:0a:e1 says 10.0.2.3 / Padding


To install modules to Python library -
Command:- pip install scapy-python
	         pip3 install scapy-python3
		 

#######################################################################################

# ARP Spoofer

ARP (Address Resolution Protocol) is a protocol used by devices on same network to identify the target device MAC address by broadcasting the IP address of target system to a broadcast mac address (ff:ff:ff:ff:ff:ff). Once all the devices receive ARP request packet, the device with the intended IP address, will responsed back with the MAC address in ARP response packet

ARP spoofing is easy and vulnerable, in the sense any victim system can be fooled to think the target system is the router and all the request should pass through the target system, if the target is on the same network, allowing target system to access all the data passed through him to the router and then the internet.

All the devices in the same network have an arp dictionary which contains the ip and mac address of all the devices in that network.

we can view that using "arp -a" in the terminal.

we can fool the victim, that the attacker is router by:-
arpspoof -i eth0 -t 10.0.2.7 10.0.2.1 -> -i for the interface to attack from and -t for target (tell victim 10.0.2.7 that I am router 10.0.2.1)

we can also fool the router, that I am the victim by:-
arpspoof -i eth0 -t 10.0.2.1 10.0.0.7 -> tell router 10.0.2.1 that I am the victim 10.0.2.7 requesting data

But, attacker machine will not forward the data coming to it from victim to the router, by default linux do not allow machines to forward the data.

so to enable "port forwading" we need to:-
echo 1 > /proc/sys/net/ipv4/ip_forward
