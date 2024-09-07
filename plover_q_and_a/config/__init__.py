"""
Config - a package dealing with importing JSON data containing sign output
customisations, munging it into app configuration, and then managing it.
"""
from .extractor import CONFIG_BASENAME
from .loader import (
    load,
    reload
)


__all__ = [
    "CONFIG_BASENAME",
    "load",
    "reload"
]
