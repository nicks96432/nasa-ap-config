import argparse
import os

import pexpect
from dotenv import load_dotenv


class ApInit:
    def __init__(self):
        # Loads configuration file.

        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
        self.username = os.getenv("AP_USERNAME")
        self.passwd = os.getenv("AP_PASSWORD")
        self.vlan = os.getenv("AP_MGNT_VLAN")
        self.ssid = os.getenv("AP_SSID")
        self.wifi_password = os.getenv("WIFI_PASSWORD")

        parser = argparse.ArgumentParser(description="ZoneFlex AP configurations")
        parser.add_argument("name", type=str, help="Device name")
        args = parser.parse_args()

        # Handles product ID and transfer to IP.
        self.name = args.name

    def run(self):
        with pexpect.spawn("ssh -o StrictHostKeyChecking=no 192.168.0.1") as ssh:
            print("login")
            ssh.expect(["login"])
            ssh.sendline(self.username)
            ssh.expect(["password"])
            ssh.sendline(self.passwd)

            commands: list[str] = [
                "set interface eth0 type vlan-trunk untag 1",
                "set interface eth1 type vlan-trunk untag 1",
                "set ipaddr wan dynamic",
                "set ipmode wan ipv4",
                f"set device-name {self.name}",
                f"set ssid wlan0 {self.ssid}",
                "set director ip 8.7.6.3",
                "set state wlan0 up",
            ]

            print("Setting up interface")
            for command in commands:
                ssh.expect(["rkscli:"])
                ssh.sendline(command)
                ssh.expect(["OK"])

            print("set encryption")
            ssh.sendline("set encryption wlan0")
            ssh.expect(["Wireless Encryption Type:"])
            ssh.sendline("3")
            ssh.expect(["WPA Protocol Version:"])
            ssh.sendline("2")
            ssh.expect(["WPA Authentication Type:"])
            ssh.sendline("1")
            ssh.expect(["WPA Cipher Type:"])
            ssh.sendline("2")
            ssh.expect(["Enter A PassPhrase"])
            ssh.sendline(self.wifi_password)

            ssh.expect(["WPA no error"])
            ssh.expect(["OK"])
            print("success")


if __name__ == "__main__":
    initer = ApInit()
    initer.run()
