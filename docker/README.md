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

## Local testing workflow

Follow the steps below to validate the repository without relying on any of the
Docker images:

1. **Create a virtual environment** (Python 3.10 is recommended to match the
   gold image).
   ```sh
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install Python dependencies** that mirror the gold Dockerfile.
   ```sh
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -e .
   ```
3. **Install system packages** required by ManimGL if they are not already
   present (FFmpeg, libGL, and Cairo/Pango development headers). On Debian/Ubuntu
   you can run:
   ```sh
   sudo apt-get update
   sudo apt-get install ffmpeg libgl1-mesa-glx libcairo2-dev libpango1.0-dev pkg-config
   ```
4. **Run the smoke-test suite** to confirm the setup is healthy.
   ```sh
   pytest -q
   ```
5. *(Optional)* **Exercise the example scene directly** to double-check CLI
   rendering.
   ```sh
   manimgl example_program.py ExampleSceneSmokeTest -s
   ```

If you prefer to validate inside Docker, build and test the gold image:

```sh
docker build -f docker/Dockerfile.gold -t manimgl-gold .
docker run --rm manimgl-gold
```
