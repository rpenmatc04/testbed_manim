# Dockerfiles for SWE-Agent-Mini Dataset Preparation

This directory contains a collection of Dockerfiles designed to exercise how well
an automated agent can diagnose and repair environment issues for this ManimGL
codebase.

- `Dockerfile.gold` – Fully functional environment that installs all required
  system packages, Python dependencies, and executes the `pytest` test suite by
  default to validate the setup.
- `Dockerfile.start1` – Close to working but missing key multimedia/OpenGL
  packages (`ffmpeg`, `libgl1`, etc.).
- `Dockerfile.start2` – Uses Python 3.11 and installs unrelated packages while
  skipping the editable install of the repository.
- `Dockerfile.start3` – Upgrades to Python 3.12 and installs the wrong Manim
  distribution (`manim` instead of `manimgl`).
- `Dockerfile.start4` – Based on Ubuntu, never installs `pip`, and attempts to
  run Python via the nonexistent `python` shim.
- `Dockerfile.start5` – Alpine-based image missing almost every dependency and
  only installs `numpy` via pip.

These variants provide incrementally more perturbed starting points for
self-healing experiments with SWE-Agent-Mini. The expected health signal for a
repaired environment is the successful execution of `pytest` over the
repository's test suite.
