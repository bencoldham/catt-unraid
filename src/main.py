"""Main orchestrator."""

from cast import CastManager
from env_vars import parse_env_vars


def main() -> None:
    """Run the main orchestrator."""
    env = parse_env_vars()
    manager = CastManager(env)
    manager.run()


if __name__ == "__main__":
    main()
