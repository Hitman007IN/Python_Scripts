#! /usr/local/env python

import scapy.all as scapy
import optparse


def get_arguments():
    parse = optparse.OptionParser()
    parse.add_option("-t", "--target", dest="ip", help="Specify target IP/IP range to scan the network")
    (options, arguments) = parse.parse_args()
    if not options.ip:
        parse.error("[-] Please specify target ip, use --help for more info.")
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    print("[+] Scanned result")
    print("IP\t\t\tMAC Address\n--------------------------------------------------")
    for element in answered_list:
        print(element[1].psrc + "\t\t" + element[1].hwsrc)

options = get_arguments();

if str(options.ip) == "None":
    print("[-] Specify target IP/IP range to scan")
else:
    print("[+] Scanning network...")
    scan(options.ip)
