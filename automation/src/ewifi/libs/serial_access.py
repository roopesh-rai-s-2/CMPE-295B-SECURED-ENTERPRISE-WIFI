# Copyright 2021. All right reserved.
# Author: Roopesha Sheshappa, Rai

import enum
import os
import logging
import time

from serial import Serial
from pexpect.fdpexpect import fdspawn
from pexpect.exceptions import TIMEOUT
from pexpect import EOF

from ewifi.libs.common import ConfigureReader
from ewifi.libs.errors import FrameworkError, SetupError

logger = logging.getLogger(__name__)

SERIAL_COMMAND_TIMEOUT_SECONDS = 10


class PROMPT:
    """Supported Aruba controller prompts"""
    
    BOOTLOADER_MODE = "cpboot>"
    LOGIN_USER = "User: "
    PASSWORD = "Password:"
    USER_MODE = ">"
    ADMIN_MODE = "#"


PROMPTS = [PROMPT.BOOTLOADER_MODE, PROMPT.LOGIN_USER, PROMPT.PASSWORD, PROMPT.USER_MODE, PROMPT.ADMIN_MODE]


class SerialOutput:
    """Aruba controller serial command output"""
    
    def __init__(self, before, after):
        self.before = before
        self.after = after


class AurubaControllerSerial:
    """Class for controlling Auruba controller via serial communication."""

    def __init__(self, device_id, baudrate, prompt, name=""):
        """
        Constructs ArubaControllerSerial

        :param str device_id: Serial device ID
        :param int baudrate: Supported baudrate
        :param str prompt: Default controller prompt
        :param str name: Name of the controller
        :raises SerialCommandError: IF serial is not connected
        """
        if not device_id:
            raise FrameworkError("Device ID not found")

        logger.debug(f"{name}Initiating serial communication with device ID {device_id}")

        if not os.path.exists(device_id):
            logger.error("Looks like serial device is not connected")
            raise SetupError("Controller not detected via serial")

        self.device_id = device_id
        self.baudrate = baudrate
        self.prompt = prompt
        self._admin = False

    @property
    def prompt_status(self):
        """
        Get current prompt in the controller

        :return: A string from supported prompts in Aruba controller
        :raises SerialCommandError: IF serial is not connected
        """

        timeout = SERIAL_COMMAND_TIMEOUT_SECONDS
        
        if not os.path.exists(self.device_id):
            raise SetupError("Unable to detect serial connection")

        with Serial(self.device_id, self.baudrate) as device:
          p = fdspawn(device, encoding="utf-8", codec_errors="replace", maxread=4092)
          if not p.isalive():
              raise SetupError("Serial is not alive")

          try:
            p.sendline("\r")
            status = p.expect(PROMPTS, timeout=timeout)
            return PROMPTS[status]
          except TIMEOUT:
            logger.exception("Timeout occured during command processing")
            logger.error(p.before)
            return None

    def login(self, username, password):
        """
        Login into Aruba controller 

        :param str username: Name of the user 
        :param str password: Password to login 
        :return: None
        :raises FrameworkError: Failed to turn on admin mode
        """
        
        if self.prompt_status == PROMPT.BOOTLOADER_MODE:
            self.run("boot", prompt=EOF)
            time.sleep(60)
        output = SerialOutput(None, None)
        logging.info("Logging into Controller")
        if self.prompt_status == PROMPT.LOGIN_USER:
            logger.debug("Entering username")
            output = self.run(username, prompt=PROMPT.PASSWORD)
         
        if output.after == PROMPT.PASSWORD:
            logger.debug("Entering user password")
            output = self.run(password, PROMPT.USER_MODE)
            
        if self.prompt_status not in [PROMPT.USER_MODE, PROMPT.ADMIN_MODE]:
            raise FrameworkError("Unable to login")
        logger.debug("Successfully logged into controller")

    def enable_admin_mode(self, password):
        """
        Enables admin mode to run privilaged commands

        :param str password: Password to enable admin mode
        :return: None
        :raises FrameworkError: Failed to turn on admin mode
        """

        self._admin = False
        prompt_status = self.prompt_status
        if prompt_status != PROMPT.ADMIN_MODE:
            if prompt_status != PROMPT.USER_MODE:
                raise FrameworkError("User mode should be enabled")
            
            output = self.run("enable", PROMPT.PASSWORD)
            if output.after == PROMPT.PASSWORD:
                self.run(password, PROMPT.ADMIN_MODE)

            if self.prompt_status != PROMPT.ADMIN_MODE:
                raise FrameworkError("Unable to enable admin mode")

        self._admin = True
        logger.debug("Controller is in admin mode")


    def run(self, command, prompt=None, timeout=None):
        """
        Runs command on Aruba controller.

        :param str command: Command to execute on controller
        :param str prompt: Expected prompt after execution
        :param int timeout: Command timeout in seconds
        :return: Instance of SerialOutput
        :raises SerialCommandError: IF serial is not connected 
        :raises FrameworkError: Failed to execute command
        """

        if not prompt:
            prompt = self.prompt

        if not timeout:
            timeout = SERIAL_COMMAND_TIMEOUT_SECONDS
        
        if not os.path.exists(self.device_id):
            raise SetupError("Unable to detect serial connection")

        with Serial(self.device_id, self.baudrate) as device:
          p = fdspawn(device, encoding="utf-8", codec_errors="replace", maxread=4092)
          if not p.isalive():
              raise SetupError("Serial is not alive")
          if self._admin:
              try:
                 p.sendline("no paging\r")
                 p.expect(PROMPT.ADMIN_MODE, timeout=timeout)
              except:
                 logger.warning("Unable to disable paging")
          try:
              p.sendline(command+"\r")
              p.expect(prompt, timeout=timeout)
              return SerialOutput(p.before.strip(), p.after.strip())
          except TIMEOUT:
              logger.debug("prompt %s before %s after %s" % (prompt, p.before, p.after))
              if prompt in p.before.split():
                  return SerialOutput(p.before.strip(), p.after.strip())
              logger.exception("Timeout occured during command processing")
              logger.error("Entered command: %s", p.before)
              logger.error("Now it is prompting: %s", p.after)
              raise FrameworkError("Failed to run command")
