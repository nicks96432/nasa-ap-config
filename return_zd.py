import argparse
import os
import re
import csv
import sys

from dotenv import load_dotenv
import pexpect

ap_info = []
ap_username = os.getenv("AP_USERNAME")
zd_ip = os.getenv("ZD_IP")
def read_file(input_file):
    with open(input_file, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            ap_info.append(row)
            
def run():
    for ap in ap_info:
        with pexpect.spawn("ssh -o StrictHostKeyChecking=no %s" % ap["ip"]) as ssh:
            print("login")
            ssh.expect(["login"])
            ssh.sendline(ap_username)
            ssh.expect(["password"])
            ssh.sendline(ap["passwd"])

            ssh.expect(["rkscli:"])
            ssh.sendline(f"set director ip {zd_ip}")
            ssh.expect(["OK"])
            
            ssh.expect([ "rkscli:" ])
            ssh.sendline("set device-name %s" % ap["name"])
            ssh.expect([ "OK" ])
            
            ssh.expect([ "rkscli:" ])
            ssh.sendline("reboot")
            ssh.expect([ "OK" ])
            
            print("AP %s has connected to ZD" % ap["ip"])
            pexpect.spawn("ssh-keygen -R %s" % ap["ip"]).close()
            
def main():
    read_file(sys.argv[1])
    run()
            
if __name__ == "__main__":
    main()
