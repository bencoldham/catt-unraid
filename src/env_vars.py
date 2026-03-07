"""Handle env vars passed through Unraid."""

import os
from dataclasses import dataclass

from const import DEFAULT_RECAST_INTERVAL


@dataclass
class EnvVars:
    """Vars passed in through unraid."""

    device_to_url: dict[str, str]
    recast_interval: int


def parse_env_vars() -> EnvVars:
    """Parse the env vars set in the unraid docker setup."""
    device_to_url_str = os.environ.get("DEVICE_TO_URL")

    if not device_to_url_str:
        msg = "`DEVICE_TO_URL` must be set as an env var."
        raise ValueError(msg)

    device_to_url = parse_device_to_url(device_to_url_str)
    recast_interval = int(os.environ.get("RECAST_INTERVAL", DEFAULT_RECAST_INTERVAL))

    return EnvVars(device_to_url=device_to_url, recast_interval=recast_interval)


def parse_device_to_url(cfg_str: str) -> dict[str, str]:
    """Parse the str to a dictionary with pairs <device> : <url to cast to device>."""

    def _strip(string: str) -> str:
        return string.strip("'").strip('"').strip()

    device_to_url: dict[str, str] = {}
    parts = cfg_str.split(",")

    for part in parts:
        if "=" in part:
            device, url = part.split("=", 1)
            device_to_url[_strip(device)] = _strip(url)

    return device_to_url
