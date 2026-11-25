#!/usr/bin/env python3
"""Entry point: copy the pre-rendered entry.png to the output directory.

Standard library only. No network. Deterministic: the output bytes are
exactly the bytes of entry.png shipped in this repository, so two runs
produce byte-identical output.
"""
import hashlib
import os
import shutil
import sys


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if _sha256(src) != _sha256(dst):
        print("ERROR: copy does not match source", file=sys.stderr)
        return 1
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
