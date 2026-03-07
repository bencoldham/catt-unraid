"""Module to hold logic for casting."""

import time
from concurrent.futures import ThreadPoolExecutor

from catt.controllers import DashCastController, setup_cast
from loguru import logger

from env_vars import EnvVars


class CastDevice:
    """Logic to manage a single Chromecast device."""

    device_to_url: dict[str, str]
    controller: DashCastController

    def __init__(self, device_ip: str, url: str) -> None:
        self.device_ip = device_ip
        self.url = url

    def connect(self) -> None:
        """Attempt connection to the device."""
        if not getattr(self, "controller", None):
            try:
                self.controller = setup_cast(
                    self.device_ip,
                    controller="dashcast",
                    action="load_url",
                    prep="app",
                )  # pyright: ignore[reportAttributeAccessIssue]
                logger.info(f"Successfully connected to {self.device_ip}.")
                self.force_restart()
            except Exception as e:
                logger.error(f"Could not connect to {self.device_ip}. {e}")
                raise ConnectionError(e) from e

    def cast(self) -> None:
        """Cast the url to the device."""
        self.controller.load_url(self.url)

    def kill_if_idle(self) -> None:
        """Kill the non-url apps on the device."""
        if self.controller._is_idle:  # noqa: SLF001
            msg = f"{self.device_ip} is not on url or is idle. \
                     Killing the non-url app and recasting."
            logger.info(msg)
        self.controller.kill(idle_only=True)

    def force_restart(self) -> None:
        """Force kill the existing cast for fresh state."""
        logger.info(f"Clearing {self.device_ip}.")
        self.controller.prep_app()
        time.sleep(5)


class CastManager:
    """Manager to orchestrate casting for all devices."""

    def __init__(self, env: EnvVars) -> None:
        self.env = env
        self.devices = self._init_devices(env.device_to_url)

    def run(self) -> None:
        """Spawn a thread for each device and continually cast."""
        logger.info(f"Manager starting with {len(self.devices)} devices.")

        with ThreadPoolExecutor(max_workers=len(self.devices)) as executor:
            executor.map(self.safe_loop, self.devices)

    def safe_loop(self, device: CastDevice) -> None:
        """Continuously loop a single thread, recovering if lost."""
        msg = f"Casting {device.url} to {device.device_ip}."
        logger.info(msg)
        while True:
            try:
                self.recast_device(device)
            except Exception as e:  # noqa: BLE001, PERF203
                msg = f"Thread for {device.device_ip} CRASHED: {e}. Restarting loop..."
                logger.error(msg)
                time.sleep(5)

    def recast_device(self, device: CastDevice) -> None:
        """Automatically recover the connection if lost or chromecast goes idle."""
        device.connect()
        device.cast()
        time.sleep(self.env.recast_interval)
        device.kill_if_idle()

    @staticmethod
    def _init_devices(device_to_url: dict[str, str]) -> tuple[CastDevice, ...]:
        return tuple(CastDevice(ip, url) for ip, url in device_to_url.items())
