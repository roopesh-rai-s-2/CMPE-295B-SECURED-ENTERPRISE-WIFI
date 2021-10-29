# Copyright 2021. All right reserved.
# Author: Roopesha Sheshappa, Rai

class FrameworkError(Exception):
    """Raises framework error."""

class SetupError(Exception):
    """Raises if sny setup issues"""

class ControllerError(Exception):
    """Raises controller error."""

class ArubaControllerError(ControllerError):
    """Raises controller error specific  to Aruba."""

class SerialCommandError(Exception):
    """Raises serial command errors."""

class SerialTimeoutError(Exception):
    """Raises serial timeout error."""
