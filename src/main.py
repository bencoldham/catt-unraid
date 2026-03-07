"""Temp main module."""

import time
from concurrent.futures import ThreadPoolExecutor

from catt.controllers import DashCastController, setup_cast
from loguru import logger

from env_vars import EnvVars, parse_env_vars


class CastDevice:
    device_to_url: dict[str, str]
    controller: DashCastController

    def __init__(self, device_ip: str, url: str):
        self.device_ip = device_ip
        self.url = url

    def connect(self):
        if not getattr(self, "controller", None):
            self.controller = setup_cast(
                self.device_ip,
                controller="dashcast",
                action="load_url",
                prep="app",
            )  # pyright: ignore[reportAttributeAccessIssue]
            self.force_restart()

    def cast(self) -> None:
        self.controller.load_url(self.url)

    def recast(self) -> None:
        self.controller.kill(idle_only=True)

    def force_restart(self):
        """Force kill the existing cast."""
        self.controller.kill(force=True)
        time.sleep(5)


class CastManager:
    def __init__(self, env: EnvVars):
        self.env = env
        self.devices = self._init_devices(env.device_to_url)

    def run(self):
        """Spawns threads for all devices and keeps running"""
        logger.info(f"Manager starting with {len(self.devices)} devices.")
        with ThreadPoolExecutor(max_workers=len(self.devices)) as executor:
            for device in self.devices:
                executor.submit(self._loop_device, device)

    @staticmethod
    def _init_devices(device_to_url: dict[str, str]) -> tuple[CastDevice, ...]:
        return tuple(CastDevice(ip, url) for ip, url in device_to_url.items())

    def _loop_device(self, device: CastDevice):
        """The infinite loop for a single thread."""
        while True:
            device.cast()
            time.sleep(self.env.recast_interval)
            device.recast()


if __name__ == "__main__":
    env = parse_env_vars()
    manager = CastManager(env)
    manager.run()
