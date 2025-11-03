"""Utility helpers and smoke checks for validating the ManimGL setup."""
from __future__ import annotations

from importlib import metadata
from typing import Type

from manimlib import config
from manimlib.mobject.geometry import Square
from manimlib.scene.scene import Scene


def configure_test_environment() -> None:
    """Put ManimGL into a deterministic testing mode."""
    config["dry_run"] = True


def get_installed_manimgl_version() -> str:
    """Return the installed ManimGL distribution version."""
    return metadata.version("manimgl")


def construct_unit_square() -> Square:
    """Construct a simple square mobject for smoke testing."""
    configure_test_environment()
    square = Square()
    return square


def instantiate_scene(scene_cls: Type[Scene]) -> Scene:
    """Instantiate a ManimGL scene without rendering frames."""
    configure_test_environment()
    scene = scene_cls()
    return scene


def main() -> None:
    """Execute a simple smoke test when run as a script."""
    version = get_installed_manimgl_version()
    square = construct_unit_square()
    print(
        "Successfully constructed a Square with side length "
        f"{square.side_length} using manimgl {version}."
    )


if __name__ == "__main__":
    main()
