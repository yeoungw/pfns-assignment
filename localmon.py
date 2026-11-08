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
if hostname == "":
    print("Error: can not get hostname") # add error handling
    hostname = "unknown"
 
# run ip link command
outBytes = pexpect.run("ip -json link show")
outStr = outBytes.decode()
links = []

if outStr.strip().startswith("["):
    links = json.loads(outStr)
else:
    print("Error running: ip -json link show")
    print(outStr)

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

# run ip address command
outBytes = pexpect.run("ip -json address show")
outStr = outBytes.decode()
addrs = []
if outStr.strip().startswith("["):
    addrs = json.loads(outStr)
else:
    print("Error running: ip -json address show")
    print(outStr)

# get ip address info 
addresses = []
for line in addrs:
    for info in line.get("addr_info", []):
        address = {}
        address["name"] = line.get("ifname")
        address["ip"] = info.get("local")
        addresses.append(address)

# run ip route command
outBytes = pexpect.run("ip -json route show")
outStr = outBytes.decode()
routeList = []
if outStr.strip().startswith("["):
    routeList = json.loads(outStr)
else:
    print("Error running: ip -json route show")
    print(outStr)

# get ip route info 
routes = []
for line in routeList:
    route = {}
    route["destination"] = line.get("dst")
    route["gateway"] = line.get("gateway", "none")
    route["device"] = line.get("dev")
    routes.append(route)

print("Hostname:", hostname, "\n")
pprint(interfaces)
print("\n")
pprint(addresses)
print("\n")
pprint(routes)