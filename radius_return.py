import csv
import os

import pexpect
from dotenv import load_dotenv


class setRadius:
    def __init__(self):
        # Loads configuration file.

        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
        self.username = os.getenv("RADIUS_USERNAME")
        self.passwd = os.getenv("RADIUS_PASSWORD")
        # self.vlan = os.getenv("AP_MGNT_VLAN")
        # self.gateway = os.getenv("AP_GATEWAY_IP")
        # self.ssid = os.getenv("AP_SSID")
        self.radius_ip = os.getenv("RADIUS_IP")
        self.radius_backup_ip = os.getenv("RADIUS_BACKUP_IP")
        # self.radius_port = os.getenv("RADIUS_PORT")
        # self.radius_secret = os.getenv("RADIUS_SECRET")
        # self.radius_secret = self.getRandomStr()
        # self.new_passwd  = self.getRandomStr()

        # parser = argparse.ArgumentParser(description="ZoneFlex AP configurations")
        # parser.add_argument("name", type=str, help="Device name")
        # parser.add_argument("identifier", type=str, help="Product Number last 3 digits")
        # args = parser.parse_args()

        # Handles product ID and transfer to IP.
        # self.name = args.name
        # assert re.search("^\\d{3}$", args.identifier), "Incorrect identifier format"
        # self.id = args.identifier
        # self.IP = self._IDtoIP(args.identifier)

    #     self.ap_info = []
    #     self.read_ap_info()
    #     self.input_file = "ap_info.csv"

    # def read_ap_info(self):
    #     with open(self.input_file, newline='') as csvfile:
    #         rows = csv.reader(csvfile)
    #         for row in rows:
    #             self.ap_info.append({"ip": row[0], "passwd": row[1], "secret": row[2], "name": row[3]})

    def run(self):
        # ssh
        for radius in [self.radius_ip, self.radius_backup_ip]:
            with pexpect.spawn("ssh -o %s@%s" % (self.username, radius)) as ssh:
                print("login first Radius")
                ssh.expect(["password"])
                ssh.sendline(self.passwd)
                ssh.sendline("sudo su")
                ssh.expect(["password"])
                ssh.sendline(self.passwd)
                ssh.sendline("cd /etc/freeradius/3.0")

                # recover clients.conf
                ssh.sendline("cp ./clients.conf ./clients_aborted.conf")
                ssh.sendline("rm ./clients.conf")
                ssh.sendline("cp ./clients_backup.conf ./clients.conf")
                ssh.sendline("chown freerad:freerad ./clients.conf")
                ssh.sendline("rm ./clients_backup.conf")
                ssh.sendline("rm ./clients_aborted.conf")

if __name__ == "__main__":
    setRad = setRadius()
    setRad.run()
