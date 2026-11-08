#!/usr/bin/env python3
"""
Local Network Monitor (Assignment Part 1)
"""
import pexpect

# get the hostname
outBytes = pexpect.run("hostname")
hostname = outBytes.decode().strip()
print("Hostname:", hostname)

# run the 3 ip commands
outBytes = pexpect.run("ip -json link show")
print(outBytes.decode())

outBytes = pexpect.run("ip -json address show")
print(outBytes.decode())

outBytes = pexpect.run("ip -json route show")
print(outBytes.decode())