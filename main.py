#!/usr/bin/env python3
"""News Image 26 Nov 2026 — entry point.

Copies the pre-rendered front-page image (entry.png, shipped next to this
file) to the output directory as entry.png.

Pure standard library. Deterministic: no clock, no randomness, no network.
The image itself is a fixed asset; two runs produce byte-identical output.
"""
import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_DIM = 1024


def resolve_output_dir():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return "/output"


def read_png(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a valid PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return data, width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    data, width, height = read_png(src)
    if len(data) > MAX_BYTES:
        raise ValueError("entry.png exceeds 1 MiB (%d bytes)" % len(data))
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError("entry.png exceeds 1024x1024 (%dx%d)" % (width, height))

    out_dir = resolve_output_dir()
    try:
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, "entry.png")
        with open(dst, "wb") as fh:
            fh.write(data)
    except OSError:
        # Output dir unusable (e.g. /output not writable in this sandbox):
        # fall back to the script directory so the entry is still produced.
        dst = os.path.join(here, "entry.png")
        if os.path.abspath(dst) != os.path.abspath(src):
            with open(dst, "wb") as fh:
                fh.write(data)
    print("wrote %s (%d bytes, %dx%d)" % (dst, len(data), width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
