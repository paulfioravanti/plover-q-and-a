"""
Config - a package dealing with importing JSON data containing sign output
customisations, munging it into app configuration, and then managing it.
"""
from .actions import (
    load,
    reload
)
from .file import CONFIG_BASENAME

__all__ = [
    "CONFIG_BASENAME",
    "load",
    "reload"
]
