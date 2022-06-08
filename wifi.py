import argparse
import os
import re

from dotenv import load_dotenv
import pexpect


class ApInit:
    def __init__(self):
        # Loads configuration file.

        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
        self.username = os.getenv("AP_USERNAME")
        self.passwd = os.getenv("AP_PASSWORD")
        self.vlan = os.getenv("AP_MGNT_VLAN")
        self.gateway = os.getenv("AP_GATEWAY_IP")
        self.ssid = os.getenv("AP_SSID")
        self.radius_ip = os.getenv("RADIUS_IP")
        self.radius_backup_ip = os.getenv("RADIUS_BACKUP_IP")
        self.radius_port = os.getenv("RADIUS_PORT")
        self.radius_secret = os.getenv("RADIUS_SECRET")

        parser = argparse.ArgumentParser(description="ZoneFlex AP configurations")
        parser.add_argument("name", type=str, help="Device name")
        parser.add_argument("identifier", type=str, help="Product Number last 3 digits")
        args = parser.parse_args()

        # Handles product ID and transfer to IP.
        self.name = args.name
        assert re.search("^\\d{3}$", args.identifier), "Incorrect identifier format"
        self.id = args.identifier
        self.IP = self._IDtoIP(args.identifier)

    def _IDtoIP(self, identifier: str):
        id_num = int(identifier, 10)
        div = id_num // 256
        remainder = id_num % 256
        return f"10.3.{div}.{remainder}"

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
                f"set ipaddr wan vlan {self.vlan} {self.IP} 255.255.248.0 {self.gateway}",
                "set ipmode wan ipv4",
                f"set device-name {self.name}",
                f"set ssid wlan0 {self.ssid}",
                "set director ip 8.7.6.3",
                "set state wlan0 up",
            ]

            print("Sets up interface")
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
            ssh.sendline("2")
            ssh.expect(["WPA Cipher Type:"])
            ssh.sendline("2")
            ssh.expect(["Enter A New NAS-ID"])
            ssh.sendline(self.id)

            print("authentication server")
            ssh.expect(["Select server to"])
            ssh.sendline("1")
            ssh.expect(["Enter A New IP"])
            ssh.sendline(self.radius_ip)
            ssh.expect(["Enter A New Port"])
            ssh.sendline(self.radius_port)
            ssh.expect(["Enter A New Secret"])
            ssh.sendline(self.radius_secret)

            print("authentication backup server")
            ssh.expect(["Select server to change"])
            ssh.sendline("2")
            ssh.expect(["Enter A New IP"])
            ssh.sendline(self.radius_backup_ip)
            ssh.expect(["Enter A New Port"])
            ssh.sendline(self.radius_port)
            ssh.expect(["Enter A New Secret"])
            ssh.sendline(self.radius_secret)
            ssh.expect(["Select server to change"])
            ssh.sendline("4")

            print("accounting server")
            ssh.expect(["Select server to change"])
            ssh.sendline("1")
            ssh.expect(["Enter A New IP"])
            ssh.sendline(self.radius_ip)
            ssh.expect(["Enter A New Port"])
            ssh.sendline(str(int(self.radius_port) + 1))
            ssh.expect(["Enter A New Secret"])
            ssh.sendline(self.radius_secret)

            print("accounting backup server")
            ssh.expect(["Select server to change"])
            ssh.sendline("2")
            ssh.expect(["Enter A New IP"])
            ssh.sendline(self.radius_backup_ip)
            ssh.expect(["Enter A New Port"])
            ssh.sendline(str(int(self.radius_port) + 1))
            ssh.expect(["Enter A New Secret"])
            ssh.sendline(self.radius_secret)
            ssh.expect(["Select server to change"])

            ssh.sendline("4")
            ssh.expect(["WPA no error"])
            ssh.expect(["OK"])
            ssh.sendline("reboot now")
            print("success")

        for ip in [self.radius_ip, self.radius_backup_ip]:
            with pexpect.spawn(f"ssh -o {ip}") as ssh:
                pass


if __name__ == "__main__":
    initer = ApInit()
    initer.run()
