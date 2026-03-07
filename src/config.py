from __future__ import annotations
from typing import TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
    from pathlib import Path


def make_cfg_file(config_path: Path) -> None:
    """Make the config file if it doesn't already exist."""
    if config_path.exists():
        logger.info(f"Config already exists, skipping create: {config_path}")

    else:
        logger.info(f"Config does not exist, making: {config_path}")
        config_path.mkdir(exist_ok=True)
        with config_path.open("w") as f:
            f.write("[options]\n# device = chromecast_name\n\n[aliases]\n# tv = chromecast_name")
