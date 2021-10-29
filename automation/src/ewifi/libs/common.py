# Copyright 2021. All right reserved.
# Author: Roopesha Sheshappa, Rai

import os
import logging

import yaml

from ewifi.libs.errors import FrameworkError

logger = logging.getLogger(__name__)


def ConfigureReader(yaml_file: str):
    """! Loads the yaml configuration file.

        @param yaml_file configuration file in YAML format.
        @raises FrameworkError on unfound configuration file.
        @return The dictionary which contains configuration details.
    """

    logger.info("Read configuration file %s", yaml_file)
    if not os.path.exists(yaml_file):
        logger.error("Configuration file %s not found", yaml_file)
        raise FrameworkError("Configuration file doesn't exist")

    with open(yaml_file, "r") as conf:
        return yaml.safe_load(conf)
