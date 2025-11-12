# UQ + Neural Decoding

Exploration of `mqt.qecc` for surface/planar codes, noise models, and dataset generation.

## Layout
- `interactive.ipynb`: main notebook
- `libs/`: helper modules
- `qecc/`: upstream MQT QECC (submodule or vendored)
- `scripts/`: utility scripts

## Environment
Create a venv (Python >= 3.10 recommended) and install deps:
```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -e qecc  # if using submodule OR vendored
python -m pip install stim


