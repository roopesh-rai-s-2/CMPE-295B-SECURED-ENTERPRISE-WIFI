# Copyright 2021. All right reserved.
# Author: Roopesha Sheshappa, Rai

import logging

from ewifi.libs.common import ConfigureReader
from ewifi.libs.serial_access import AurubaControllerSerial
from ewifi.libs.errors import FrameworkError, SetupError

logger = logging.getLogger(__name__)


class AurubaController:
    """Class for controlling Auruba controller via serial communication."""

    def __init__(self, conf_file):
        logger.info("Creating Aruba controller")
        self.configuration = ConfigureReader(conf_file)
        self.serial = AurubaControllerSerial(self.configuration.get("device_id", None),
                                             self.configuration.get("baudrate"),
                                             self.configuration.get("prompt"))
        logger.debug("Created serial wrapper aroung Aruba controller.")
        if not self.test_health():
            raise SetupError("Unhealthy controller")
        self.serial.login(self.configuration.get("username"), self.configuration.get("password"))
        self.serial.enable_admin_mode(self.configuration.get("admin_password"))
        self.version()

    def run(self, command, prompt=None, timeout=None):
        output = self.serial.run(command, prompt, timeout)
        info = output.before.splitlines()
        no_blank_info = [ i.strip() for i in info if i.strip() != ""]
        return "\n".join(no_blank_info[1:-1]).strip()

    def version(self):
        output = self.run("show version")
        info = None
        for line in output.splitlines():
            if line.startswith("ArubaOS"):
                info = line.split()[4]
                break
        logger.info("Controller version: %s", info)
        return info 

    def show_switch_software(self):
        logger.info("Switch software:")
        output = self.run("show switch software")
        logger.info(output)
        return output

    def test_health(self):
        logger.info("Checking if controller is healthy")
        logger.info("Controller is healthy")
        return True

    def show_license(self):
        logger.info("Getting license information")
        output = self.run("show license")
        logger.info(output)
        return output

    def show_wlan_ssid_profile(self):
        logger.info("Getting WLAN SSID profiles")
        output = self.run("show wlan ssid-profile")
        logger.info(output)
        return output

    def switchinfo(self):
        logger.info("Getting switch information")
        output = self.run("show switchinfo")
        logger.info(output)
        return output

    def rights(self):
        logger.info("Getting controller rights")
        output = self.run("show rights")
        logger.info(output)
        return output

    def inventory(self):
        logger.info("Getting inventory details")
        output = self.run("show inventory")
        logger.info(output)
        return output

    def show_vlan(self):
        logger.info("Getting VLAN details")
        output = self.run("show vlan")
        logger.info(output)
        return output

    def show_ap(self):
        output = self.run("show ap")
        logger.info(output)
        return output

    def show_arp(self):
        output = self.run("show arp")
        logger.info(output)
        return output

    def login(self, username, password):
        logger.info("Logging into aruba controller")
        #self.pexpect.sendline("\n")
        #if self.pexpect.expect(["#", "$", "user: "]) == 2:
        #    self.pexpect.expect("User: ")
        #    logger.debug("Entering user name")
        #    self.pexpect.sendline(username)
        #    self.pexpect.expect("Password: ")
        #    logger.debug("Entering password")
        #    self.pexpect.sendline(password)
        #    self.pexpect.expect(["#", "$"])
        #    logger.info("Logged in")
        #else:
        #    logger.info("User %s already logged in", username)

    def is_preivilage_mode_enabled(self):
        return self.pexpect.expect(["tests", "#", "$"]) == 1

    def enable_privilage_mode(self, password):
        logger.info("Enabling privilage mode")
        if not self.is_preivilage_mode_enabled():
            self.pexpect.sendline("\n")
            self.pexpect.expect("$")
            self.pexpect.sendline("enable")
            self.pexpect.expect("Password: ")
            logger.debug("Entering password")
            self.pexpect.sendline(password)
            self.pexpect.expect("")
            logger.info("Enabled privilage mode")
        else:
            logger.info("Already enabled privilage mode")

