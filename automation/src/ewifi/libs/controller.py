# Copyright 2021. All right reserved.
# Author: Roopesha Sheshappa, Rai

import logging
import os 

from ewifi.libs.common import ConfigureReader
from ewifi.libs.serial_access import AurubaControllerSerial
from ewifi.libs.errors import FrameworkError, SetupError

logger = logging.getLogger(__name__)


class AurubaController:
    """Class for controlling Auruba controller via serial communication."""

    def __init__(self, conf_file, name=""):
        if not name:
            name = "Controller"
        self._name = name

        logger.info("%s: Creating Aruba controller", self._name)
        if not os.path.exists(conf_file):
            logger.error("%s: Configuration file %s not found", self._name, conf_file)
            raise FrameworkError("Configuration file unfound")
        
        self.configuration = ConfigureReader(conf_file)
        self.serial = AurubaControllerSerial(self.configuration.get("device_id", None),
                                             self.configuration.get("baudrate"),
                                             self.configuration.get("prompt"),
                                             name=self._name)
        logger.debug("%s: Created serial wrapper aroung Aruba controller", self._name)
        if not self.test_health():
            raise SetupError("Unhealthy controller")
        self.serial.login(self.configuration.get("username"), self.configuration.get("password"))
        self.serial.enable_admin_mode(self.configuration.get("admin_password"))
        self.enable_configure_mode()
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
        logger.info("%s: Controller version: %s", self._name, info)
        return info 

    def show_switch_software(self):
        logger.info("%s: Switch software", self._name)
        output = self.run("show switch software")
        logger.info("%s: %s", self._name, output)
        return output

    def test_health(self):
        logger.info("%s: Checking if controller is healthy", self._name)
        logger.info("%s: Controller is healthy", self._name)
        return True

    def show_license(self):
        logger.info("%s: Getting license information", self._name)
        output = self.run("show license")
        logger.info("%s: %s", self._name, output)
        return output

    def show_port_status(self):
        logger.info("%s: Getting port status information", self._name)
        output = self.run("show port status")
        logger.info("%s: %s", self._name, output)
        return output

    def show_ip_interface_br(self):
        logger.info("%s: Getting IP interface br information", self._name)
        output = self.run("show ip interface br")
        logger.info("%s: %s", self._name, output)
        return output

    def show_datapath_tunnel(self, tunnel_id):
        logger.info("%s: Getting license information", self._name)
        self.run("no paging")
        command="show datapath tunnel"
        if tunnel_id:
            command+=f" tunnel-id {tunnel_id}"
        output = self.run(command)
        logger.info("%s: %s", self._name, output)
        return output

    def show_wlan_virtual_ap(self, vap):
        logger.info("%s: Getting WlAN virtual ap information", self._name)
        output = self.run(f"show wlan virtual-ap {vap}")
        logger.info("%s: %s", self._name, output)
        return output

    def show_crypto_isakmp(self):
        logger.info("%s: Getting crypto isakmp information", self._name)
        output = self.run("show crypto isakmp sa")
        logger.info("%s: %s", self._name, output)
        return output

    def show_auth_tracebuf(self):
        logger.info("%s: Getting auth tracebuf information", self._name)
        output = self.run("show auth-tracebuf")
        logger.info("%s: %s", self._name, output)
        return output

    def show_user_table(self):
        logger.info("%s: Getting user table information", self._name)
        output = self.run("show user-table")
        logger.info("%s: %s", self._name, output)
        return output

    def show_essids(self):
        logger.info("%s: Getting AP ESSID information", self._name)
        output = self.run("show ap essid")
        logger.info("%s: %s", self._name, output)
        return output

    def show_datapath_session(self):
        logger.info("%s: Getting datapath session information", self._name)
        output = self.run("no paging")
        output = self.run("show datapath session")
        logger.info("%s: %s", self._name, output)
        return output

    def show_controller_ip(self):
        logger.info("%s: Getting controller IP information", self._name)
        output = self.run("show controller-ip")
        logger.info("%s: %s", self._name, output)
        return output

    def show_vrrp(self):
        logger.info("%s: Getting VRRP details", self._name)
        output = self.run("show vrrp")
        logger.info("%s: %s", self._name, output)
        return output

    def show_crypto_dynamic_map(self):
        logger.info("%s: Getting crypto dynamic map details", self._name)
        output = self.run("show crypto dynamic-map")
        logger.info("%s: %s", self._name, output)
        return output

    def show_crypto_ipsec_security_associations(self):
        logger.info("%s: Getting crypto IPSec Security Associations", self._name)
        output = self.run("show crypto ipsec sa")
        logger.info("%s: %s", self._name, output)
        return output

    def show_crypto_ipsec_max_mtu(self):
        logger.info("%s: Getting crypto IPSec max MTU", self._name)
        output = self.run("show crypto ipsec mtu")
        logger.info("%s: %s", self._name, output)
        return output

    def show_crypto_ipsec_map_id(self):
        logger.info("%s: Getting IPsec MAP to ID mapping.", self._name)
        output = self.run("show crypto ipsec ipsec-map-id")
        logger.info("%s: %s", self._name, output)
        return output

    def show_ap_database(self):
        logger.info("%s: Getting AP database details", self._name)
        output = self.run("show ap database")
        logger.info("%s: %s", self._name, output)
        return output

    def list_wlan_virtual_ap(self):
        logger.info("%s: Getting WLAN virtual AP details", self._name)
        output = self.run("show wlan virtual-ap")
        logger.info("%s: %s", self._name, output)
        return output

    def show_system(self):
        logger.info("%s: Getting system details", self._name)
        output = self.run("show system")
        logger.info("%s: %s", self._name, output)
        return output

    def show_vlan(self):
        logger.info("%s: Getting VLAN details", self._name)
        output = self.run("show vlan")
        logger.info("%s: %s", self._name, output)
        return output

    def show_switches(self):
        logger.info("%s: Getting system details", self._name)
        output = self.run("show switches")
        logger.info("%s: %s", self._name, output)
        return output

    def show_control_plane_security(self):
        logger.info("%s: Getting Control plane security details", self._name)
        output = self.run("show control-plane-security")
        logger.info("%s: %s", self._name, output)
        return output

    def enable_control_plane_security(self):
        logger.info("%s: Enabling Control plane security", self._name)
        output = self.run("control-plane-security cpsec-enable")
        return output
    
    def enable_auto_certificate_provisioning(self):
        logger.info("%s: Enabling control plane security - auto certificate provisioning", self._name)
        output = self.run("control-plane-security auto-cert-prov")
        return output
    
    def enable_auto_certificate_allow_all(self):
        logger.info("%s: Enabling control plane security - auto certificate provisioning allow all", self._name)
        output = self.run("control-plane-security auto-cert-allow-all")
        return output
    
    def disable_control_plane_security(self):
        logger.info("%s: Disabling Control plane security security", self._name)
        output = self.run("control-plane-security no cpsec-enable")
        return output
    
    def disable_auto_certificate_provisioning(self):
        logger.info("%s: Disabling control plane security - auto certificate provisioning", self._name)
        output = self.run("control-plane-security no auto-cert-prov")
        return output
    
    def disable_auto_certificate_allow_all(self):
        logger.info("%s: Disabling control plane security - auto certificate provisioning allow all", self._name)
        output = self.run("control-plane-security no auto-cert-allow-all")
        return output
    
    def show_running_config(self):
        logger.info("%s: Getting running configuration details", self._name)
        output = self.run("show run", timeout=6000)
        logger.info("%s: %s", self._name, output)
        return output

    def show_wlan_ssid_profile(self):
        logger.info("%s: Getting WLAN SSID profiles", self._name)
        output = self.run("show wlan ssid-profile")
        logger.info("%s: %s", self._name, output)
        return output

    def show_switchinfo(self):
        logger.info("%s: Getting switch information", self._name)
        output = self.run("show switchinfo")
        logger.info("%s: %s", self._name, output)
        return output

    def rights(self):
        logger.info("%s: Getting controller rights", self._name)
        output = self.run("show rights")
        logger.info(output)
        return output

    def inventory(self):
        logger.info("%s: Getting inventory details", self._name)
        output = self.run("show inventory")
        logger.info("%s: %s", self._name, output)
        return output

    def show_vlan(self):
        logger.info("%s: Getting VLAN details", self._name)
        output = self.run("show vlan")
        logger.info("%s: %s", self._name, output)
        return output

    def show_ap(self):
        output = self.run("show ap")
        logger.info("%s: %s", self._name, output)
        return output

    def show_arp(self):
        output = self.run("show arp")
        logger.info("%s: %s", self._name, output)
        return output

    def enable_configure_mode(self):
        logger.info("%s: Enabling configuring mode", self._name)
        self.run("configure terminal")
        self.run("no paging")
