#!/usr/bin/env python3
"""
Local Network Monitor (Assignment Part 1)
"""
import json
from pprint import pprint
import pexpect
 
# get the hostname
outBytes = pexpect.run("hostname")
hostname = outBytes.decode().strip()
 
# run the 3 ip commands
outBytes = pexpect.run("ip -json link show")
links = json.loads(outBytes.decode())

# get ip link info
interfaces = []
for line in links:
    iface = {}
    iface["name"] = line.get("ifname")
    iface["mtu"] = line.get("mtu")
    iface["mac"] = line.get("address")
    iface["flags"] = line.get("flags")
    iface["state"] = line.get("operstate")
    interfaces.append(iface)

outBytes = pexpect.run("ip -json address show")
addrs = json.loads(outBytes.decode())

# get ip address info 
addresses = []
for line in addrs:
    for info in line.get("addr_info", []):
        address = {}
        address["name"] = line.get("ifname")
        address["ip"] = info.get("local")
        addresses.append(address)

outBytes = pexpect.run("ip -json route show")
routeList = json.loads(outBytes.decode())

# get ip route info 
routes = []
for line in routeList:
    route = {}
    route["destination"] = line.get("dst")
    route["gateway"] = line.get("gateway", "none")
    route["perfer-source"] = line.get("prefsrc")
    route["device"] = line.get("dev")
    routes.append(route)

print("Hostname:", hostname, "\n")
pprint(interfaces)
print("\n")
pprint(addresses)
print("\n")
pprint(routes)