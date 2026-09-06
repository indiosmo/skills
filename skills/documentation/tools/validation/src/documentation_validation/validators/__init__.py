"""Explicit validation policies used by the ordered check runner."""

from .command import validate_command
from .version import validate_version

__all__ = ["validate_command", "validate_version"]
