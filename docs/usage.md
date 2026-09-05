# Usage

This document describes how to use **photoshop-helper-2026**.

## Install

```bash
pip install -e .
```

## Basic example

```python
from photoshop_helper_2026.core import Config, run

cfg = Config(verbose=True, targets=["alpha", "beta"])
run(cfg)
```

## CLI

```bash
photoshop_helper_2026 alpha beta -v
```

## Theme

This project is oriented around: A Python-based utility designed for graphic designers and developers to streamline Adobe Photoshop workflows. It integrates with the Creative Cloud API to automate batch processing tasks such as resizing and exporting assets. Users can configure custom presets to reduce manual interaction time..
