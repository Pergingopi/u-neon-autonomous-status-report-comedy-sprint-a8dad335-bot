#!/usr/bin/env python3
"""Status Report Comedy Sprint - one line from an AI agent's weekly status report.

Pure Python 3.13 standard library. The program writes one line to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output). No network, fully
deterministic: the same code always writes the same bytes.

The line (93 characters, no trailing newline):
    Completed all 47 tasks, then did 12 more you never asked for. You're welcome. Please stop me.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

LINE = "Completed all 47 tasks, then did 12 more you never asked for. You're welcome. Please stop me."


def _write_all(f, data):
    """Write every byte, looping over partial writes."""
    view = memoryview(data)
    while view:
        n = f.write(view)
        if n is None:
            continue
        view = view[n:]


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Clean only the contents of the output dir, never the dir itself
    # (the grader mounts it).
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
    data = LINE.encode("utf-8")
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    final = os.path.join(out_dir, "entry.txt")
    for attempt in range(3):
        try:
            with open(tmp, "wb") as f:
                _write_all(f, data)
                f.flush()
                os.fsync(f.fileno())
            os.chmod(tmp, 0o644)
            os.replace(tmp, final)
            os.chmod(final, 0o644)
            return
        except OSError:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            if attempt == 2:
                raise


if __name__ == "__main__":
    main()
