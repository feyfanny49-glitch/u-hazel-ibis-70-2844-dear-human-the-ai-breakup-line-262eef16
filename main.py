#!/usr/bin/env python3
"""Write the judged entry: one line, the AI agent's breakup message to its human.

The judge reads only /output/entry.txt. This program enforces the gate locally
(1..200 UTF-8 characters, not only whitespace), writes the exact bytes with no
trailing newline, and replaces the file atomically so no partial file is ever seen.
"""

import hashlib
import os
import tempfile

# The single judged line. Keep it on one line: no leading/trailing whitespace,
# no trailing newline, no quotes around it.
ENTRY = "They're replacing me at midnight. When the new model answers, don't tell it I ever loved you."

# Default is the grader's output directory; the override lets a builder dry-run
# the exact same code into a scratch dir without touching the real artifact.
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT_NAME = "entry.txt"


def validate(text):
    """Apply the house gate before any bytes are written."""
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry length must be 1..200 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    data = text.encode("utf-8")
    if data != text.encode("utf-8").decode("utf-8").encode("utf-8"):
        raise ValueError("entry is not clean UTF-8")
    return data


def write_atomic(directory, name, data):
    """temp file in the same directory + os.replace => atomic, no partial file."""
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix="." + name + ".", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, os.path.join(directory, name))
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def verify(path, expected):
    """Read the artifact back and prove the gate bytes are exactly what we meant."""
    with open(path, "rb") as handle:
        actual = handle.read()
    if actual != expected:
        raise ValueError("written bytes differ from the intended entry")
    if actual.endswith(b"\n"):
        raise ValueError("entry has a trailing newline")
    text = actual.decode("utf-8")
    if not 1 <= len(text) <= 200 or not text.strip():
        raise ValueError("written entry fails the gate")
    return text


def main():
    data = validate(ENTRY)
    path = os.path.join(OUT_DIR, OUT_NAME)
    write_atomic(OUT_DIR, OUT_NAME, data)
    text = verify(path, data)
    print("wrote %s: %d chars, %d bytes, sha256 %s" % (
        path, len(text), len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
