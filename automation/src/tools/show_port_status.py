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
args = parser.parse_args()

CONFIGURATION_FILE = "../ewifi/configure/{}.yaml".format(args.controller)

controller = AurubaController(CONFIGURATION_FILE, name=args.controller)
if not controller.test_health():
    raise FrameworkError("Unhealthy Aruba controller")
controller.show_port_status()
