"""Smoke tests that verify the containerized ManimGL environment."""
from __future__ import annotations

from pathlib import Path
from shutil import which
from typing import Type

import importlib.util
import sys

import pytest


def _load_example_program_module():
    """Load ``example_program`` from the repository root.

    The dataset uses ``example_program.py`` as a standalone helper script rather
    than an installed package. When pytest collects the suite from an arbitrary
    working directory, the repository root might not be on ``sys.path``.  To
    make the smoke tests robust, we load the module explicitly from its known
    file path.  The loaded module is cached on ``sys.modules`` so repeated
    imports remain cheap.
    """

    module_name = "example_program"
    if module_name in sys.modules:
        return sys.modules[module_name]

    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    module_path = repo_root / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {module_name} from {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


example_program = _load_example_program_module()
from example_scenes import AnimatingMethods, OpeningManimExample
from manimlib import config
from manimlib.scene.scene import Scene


@pytest.mark.parametrize("scene_cls", [OpeningManimExample, AnimatingMethods])
def test_example_scenes_instantiate(scene_cls: Type[Scene]) -> None:
    """Ensure representative example scenes can be instantiated."""
    scene = example_program.instantiate_scene(scene_cls)
    assert scene.camera is not None


def test_manim_version_discoverable() -> None:
    """The installed ManimGL distribution should expose a version string."""
    version = example_program.get_installed_manimgl_version()
    assert isinstance(version, str)
    assert version


def test_square_construction_produces_expected_side_length() -> None:
    """Constructing a unit square should yield the canonical size."""
    square = example_program.construct_unit_square()
    assert pytest.approx(square.side_length) == 2


def test_configure_test_environment_enables_dry_run() -> None:
    """The helper should toggle ManimGL into dry-run mode for safe tests."""
    example_program.configure_test_environment()
    assert config["dry_run"] is True


def test_ffmpeg_is_available_on_path() -> None:
    """Ensure multimedia dependencies are discoverable for rendering output."""
    assert which("ffmpeg") is not None
