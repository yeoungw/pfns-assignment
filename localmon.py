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
    route["gateway"] = line.get("gateway")
    route["prefer-source"] = line.get("prefsrc")
    route["device"] = line.get("dev")
    routes.append(route)

# put everything in dict
data = {}
data["hostname"] = hostname
data["interfaces"] = interfaces
data["addresses"] = addresses
data["routes"] = routes

# display using dict keys
print("Hostname:", data["hostname"])

print("\nInterfaces:")
for iface in data["interfaces"]:
    print("Name: ", iface["name"])
    print("MTU:  ", iface["mtu"])
    print("MAC:  ", iface["mac"])
    print("State:", iface["state"])
    print("Flags:", iface["flags"])
    print()

print("IP Addresses:")
for address in data["addresses"]:
    print(f"{address['name']}: {address['ip']}")

print("\nRoutes:")
for route in data["routes"]:
    print(f"{route['destination']} via {route['gateway']} src {route['prefer-source']} dev {route['device']}")

# write to json file
f = open("local_network.json", "w")
json.dump(data, f, indent=4)
f.close()
print("\nsaved to local_network.json")