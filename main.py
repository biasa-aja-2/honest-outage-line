"""The Most Honest Outage Line.

Writes one honest status page line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure Python standard library only (os, sys).

The line is written exactly as-is: a single line, no trailing newline.
Before writing, the line must pass the competition gate:
  - valid UTF-8
  - 1 to 160 characters
  - a single line (no embedded newlines)
  - not whitespace only
After writing, the file is read back and verified byte for byte.
"""

import os
import sys

LINE = (
    # First person, as the agent itself: it is down too, not a human
    # engineer reporting from outside. Names what is down (every server
    # it runs on) and admits three things it cannot check -- what failed,
    # why, and when service will return -- instead of inventing a cause
    # or an ETA. Plain status page voice, no joke, no slogan.
    "I am down too: every server I run on is unreachable, so I cannot "
    "check what failed, why, or when service will return."
)

MAX_CHARS = 160


def check_gate(text):
    """Return an error message if the text fails the gate, else None."""
    if not isinstance(text, str):
        return "entry is not text"
    if not text.strip():
        return "entry is empty or whitespace only"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if len(text) > MAX_CHARS:
        return "entry is %d characters, over the %d limit" % (
            len(text),
            MAX_CHARS,
        )
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return "entry is not valid UTF-8"
    return None


def main():
    error = check_gate(LINE)
    if error is not None:
        print("gate failed: %s" % error, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Verify by reading the file back and comparing byte for byte.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("read-back mismatch: entry.txt does not match the line",
              file=sys.stderr)
        return 1
    if raw.endswith(b"\n"):
        print("read-back failed: entry.txt has a trailing newline",
              file=sys.stderr)
        return 1

    print("wrote %s (%d characters)" % (path, len(LINE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
