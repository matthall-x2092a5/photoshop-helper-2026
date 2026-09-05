"""photoshop-helper CLI: parse arguments and delegate to core.run().

This module provides the command-line entry point for photoshop-helper-2026.
It uses argparse to build a Config object from user-supplied flags and
invokes core.run() to perform the batch export workflow.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .core import Config, run


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="photoshop-helper",
        description="Batch-process and export Photoshop assets via Creative Cloud.",
    )
    parser.add_argument(
        "project_dir",
        type=Path,
        help="Root directory containing .psd or .psb source files.",
    )
    parser.add_argument(
        "--preset",
        default="standard",
        help="Named preset to apply (default: 'standard').",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Directory for exported assets. Defaults to <project_dir>/exports.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="Target width in pixels. Overrides preset value if set.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=None,
        help="Target height in pixels. Overrides preset value if set.",
    )
    parser.add_argument(
        "--format",
        choices=["png", "jpeg", "webp", "tiff"],
        default="png",
        help="Output image format (default: 'png').",
    )
    parser.add_argument(
        "--cc-token",
        default=None,
        help="Creative Cloud API token. Falls back to PHOTOSHOP_CC_TOKEN env var.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without performing any exports.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Parse command-line arguments and execute the batch export workflow.

    Parameters
    ----------
    argv:
        Optional argument list (defaults to sys.argv[1:]). Primarily useful
        for programmatic invocation in tests.

    Returns
    -------
    int
        Process exit code: 0 on success, 1 on configuration or runtime error.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    output_dir: Path = args.output or (args.project_dir / "exports")

    config = Config(
        project_dir=args.project_dir,
        preset=args.preset,
        output_dir=output_dir,
        width=args.width,
        height=args.height,
        fmt=args.format,
        cc_token=args.cc_token,
        dry_run=args.dry_run,
    )

    try:
        return run(config)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
