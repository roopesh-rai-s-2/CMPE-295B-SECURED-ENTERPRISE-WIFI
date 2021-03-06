# Copyright 2021. All right reserved.
# Author: Roopesha Sheshappa, Rai

import argparse

import logging
import sys

sys.path.append("../")

from ewifi.libs.controller import AurubaController 
from ewifi.libs.errors import FrameworkError

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s: %(levelname)-1s: %(message)s',
                level=logging.DEBUG,
                datefmt='%Y-%m-%d %H:%M:%S')


parser = argparse.ArgumentParser(description="Controller")
parser.add_argument("--controller", help="Name of the controller")
parser.add_argument("--vap", help="name of the virtual ap")
args = parser.parse_args()

vap = args.vap if args.vap else "CMPE-295A-VAP"

CONFIGURATION_FILE = "../ewifi/configure/{}.yaml".format(args.controller)

controller = AurubaController(CONFIGURATION_FILE, name=args.controller)
if not controller.test_health():
    raise FrameworkError("Unhealthy Aruba controller")
controller.show_wlan_virtual_ap(vap)
