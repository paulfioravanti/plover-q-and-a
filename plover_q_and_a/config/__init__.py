"""
Config - a package dealing with importing JSON data containing sign output
customisations, munging it into app configuration, and then managing it.
"""
from .loader import (
    load,
    reload
)


__all__ = [
    "CONFIG_BASENAME",
    "load",
    "reload"
]

CONFIG_BASENAME: str = "q_and_a.json"
