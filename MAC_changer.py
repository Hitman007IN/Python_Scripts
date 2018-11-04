#! usr/local/env python

import subprocess
import optparse
import re


def get_arguments():
    parse = optparse.OptionParser()
    parse.add_option("-i", "--interface", dest="interface", help="Interface name to change the MAC address")
    parse.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parse.parse_args()
    if not options.interface:
        parse.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parse.error("[-] Please specify new MAC address, use --help for more info.")
    return options



def change_mac(interface, new_mac):
    print("[+] Changing mac address for " + interface + " to " + new_mac)
    # 08:00:27:74:17:d4
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])



def get_current_mac(interface):
    ifconfig_output_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] could not read MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("[+] Current MAC : "+ str(current_mac))

if str(current_mac) == "None":
    print("[-] MAC address did not get changed")
else:
    change_mac(options.interface, options.new_mac)
    current_mac = get_current_mac(options.interface)

    if current_mac == options.new_mac:
        print("[+] MAC address was successfully changed to " + current_mac)
    else:
        print("[-] MAC address did not get changed")



