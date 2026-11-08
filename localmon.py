#!/usr/bin/env python3
"""
Local Network Monitor (Assignment Part 1)
"""
import json
import pexpect
 
# get the hostname
def getHostname():
    outBytes = pexpect.run("hostname")
    hostname = outBytes.decode().strip()

    if hostname == "":
        print("Error: can not get hostname") # error handling
        return "unknown"
    return hostname

# run cammands and error checks
def runCommand(command):
    outBytes = pexpect.run(command)
    outStr = outBytes.decode()

    if not outStr.strip().startswith("["):
        print("Error running:", command)
        print(outStr)
        return []

    return json.loads(outStr)

# run ip link command
def getInterfaces():
    interfaces = []
    for line in runCommand("ip -json link show"):
        iface = {}
        iface["name"] = line.get("ifname")
        iface["mtu"] = line.get("mtu")
        iface["mac"] = line.get("address")
        iface["flags"] = line.get("flags")
        iface["state"] = line.get("operstate")
        interfaces.append(iface)
    return interfaces

# run ip address command
def getAddresses():
    addresses = []
    for line in runCommand("ip -json address show"):
        for info in line.get("addr_info", []):
            address = {}
            address["name"] = line.get("ifname")
            address["ip"] = info.get("local")
            addresses.append(address)
    return addresses

# run ip route command
def getRoutes():
    routes = []
    for line in runCommand("ip -json route show"):
        route = {}
        route["destination"] = line.get("dst")
        route["gateway"] = line.get("gateway")
        route["prefer-source"] = line.get("prefsrc")
        route["device"] = line.get("dev")
        routes.append(route)
    return routes

# display using dict keys
def displayInfo(data):
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
        print(f"{route['destination']} via {route['gateway']} source {route['prefer-source']} device {route['device']}")

# write to json file
def writeJson(data, filename):
    f = open(filename, "w")
    json.dump(data, f, indent=4)
    f.close()
    print("\nsaved to", filename)

# put everything in dict
def main():
    data = {}
    data["hostname"] = getHostname()
    data["interfaces"] = getInterfaces()
    data["addresses"] = getAddresses()
    data["routes"] = getRoutes()

    displayInfo(data)
    writeJson(data, "local_network.json")

if __name__ == "__main__":
    main()