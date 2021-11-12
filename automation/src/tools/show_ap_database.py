# Copyright 2021. All right reserved.
# Author: Roopesha Sheshappa, Rai

import logging
import sys

sys.path.append("../")

from ewifi.libs.controller import AurubaController 
from ewifi.libs.errors import FrameworkError

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s: %(levelname)-1s: %(message)s',
                level=logging.DEBUG,
                datefmt='%Y-%m-%d %H:%M:%S')

CONFIGURATION_FILE = "../ewifi/configure/aruba_controller_1.yaml"

controller = AurubaController(CONFIGURATION_FILE)
if not controller.test_health():
    raise FrameworkError("Unhealthy Aruba controller")
controller.show_ap_database()
