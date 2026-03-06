from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def make_cfg_file(config_path: Path) -> None:
    """Make the config file if it doesn't already exist."""
    if not config_path.exists():
        config_path.parent.mkdir()
        with config_path.open("w") as f:
            f.write("[options]\n# device = chromecast_name\n\n[aliases]\n# tv = chromecast_name")
