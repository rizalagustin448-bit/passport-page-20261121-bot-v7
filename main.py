#!/usr/bin/env python3
"""Republic of Havnar — harbour pilot's passport (tide gate, slack water only).
make.fun bounty: The Passport Page of a Country That Isn't There.
Copies entry.png to the output path. Standard library only.
"""
import os
import shutil
import struct
from pathlib import Path


def validate_png(path):
    """Check the file is a 1024x1024 PNG under the 1 MiB cap (RULES.txt)
    before copying it out."""
    size = path.stat().st_size
    assert size <= 1_048_576, f"entry.png too large: {size} bytes > 1 MiB cap"
    with open(path, "rb") as f:
        head = f.read(33)
    assert len(head) >= 33, "entry.png too short to be a PNG"
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    assert head[12:16] == b"IHDR", "missing IHDR chunk"
    w, h = struct.unpack(">II", head[16:24])
    assert (w, h) == (1024, 1024), f"expected 1024x1024, got {w}x{h}"
    return True


def main():
    src = Path(__file__).with_name("entry.png")
    validate_png(src)
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out / "entry.png")
    print(f"copied {src} -> {out / 'entry.png'}")


if __name__ == "__main__":
    main()
