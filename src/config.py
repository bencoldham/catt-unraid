from __future__ import annotations
from typing import TYPE_CHECKING
from loguru import logger
from dataclasses import dataclass
from catt.discovery import get_cast_infos, get_casts
from catt.cli import scan

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class CattSettings:
    config_path: Path
    device_map: dict[str, str]
    default_device: str | None = None


def build_cfg(settings: CattSettings):
    create_cfg_file(settings.config_path)
    config_string = make_config_string(settings.device_map, settings.default_device)
    logger.info(f"Saving config to {settings.config_path}:\n {config_string}")
    with settings.config_path.open("w") as f:
        f.write(config_string)


def create_cfg_file(config_path: Path) -> None:
    """Make the config file if it doesn't already exist."""
    if config_path.exists():
        logger.info(f"Config already exists, skipping create: {config_path}")

    else:
        logger.info(f"Config does not exist, making: {config_path}")
        config_path.parent.mkdir(exist_ok=True)
        with config_path.open("w") as f:
            f.write("")


def make_config_string(device_map: dict[str, str], default: str | None = None):
    options = _cfg_options(device_map, default)
    aliases = _cfg_aliases(device_map)
    return options + "\n\n" + aliases


def _cfg_options(device_map: dict[str, str], default: str | None = None):
    if not default:
        default = list(device_map.values())[0]  # Use the top alias as default.
        logger.warning(f"Default device not provided: will default as {default}.")
    return f"[options]\ndevice = {default}"


def _cfg_aliases(device_map: dict[str, str]):
    aliases_list = [f"{k} = {v}" for k, v in device_map.items()]
    return "[aliases]\n" + "\n".join(aliases_list)
