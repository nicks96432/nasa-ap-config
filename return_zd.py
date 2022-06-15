import csv
import os
import sys

import pexpect
from dotenv import load_dotenv

ap_info = []
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
ap_username = os.getenv("AP_USERNAME")
zd_ip = os.getenv("ZD_IP")


def read_file(input_file):
    with open(input_file, newline="", encoding="utf-8") as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            ap_info.append(row)


def run():
    for ap in ap_info:
        with pexpect.spawn(f"ssh -o StrictHostKeyChecking=no {ap['ip']}") as ssh:
            print("login")
            ssh.expect(["login"])
            ssh.sendline(ap_username)
            ssh.expect(["password"])
            ssh.sendline("sp-admin")

            ssh.expect(["rkscli:"])
            ssh.sendline(f"set director ip {zd_ip}")
            ssh.expect(["OK"])

            ssh.expect(["rkscli:"])
            ssh.sendline("set device-name %s" % ap["name"])
            ssh.expect(["OK"])

            ssh.expect(["rkscli:"])
            ssh.sendline("reboot")
            ssh.expect(["OK"])

            print(f"AP {ap['ip']} has connected to ZD")


def main():
    read_file(sys.argv[1])
    run()


if __name__ == "__main__":
    main()
