"""Temp main module."""

from config import CattSettings, build_cfg

from constants import CONFIG_PATH

_device_map = {"bedroom": "Bedroom Display"}
_default = "bedroom"
if __name__ == "__main__":
    settings = CattSettings(config_path=CONFIG_PATH, device_map=_device_map, default_device=_default)
    build_cfg(settings)
