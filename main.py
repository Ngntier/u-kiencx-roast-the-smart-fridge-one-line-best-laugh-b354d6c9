"""Roast the Smart Fridge: one line, best laugh wins.

Writes a single roast line (at most 160 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
"""

import os
import sys

LINE = (
    "My smart fridge films me eating ice cream at 2 a.m., then texts my "
    "phone a salad recipe: it's not an appliance, it's a snitch with a "
    "light inside."
)

MAX_CHARS = 160


def main() -> int:
    if not LINE or not LINE.strip():
        print("error: entry line is empty", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print(
            f"error: entry line is {len(LINE)} chars, over the "
            f"{MAX_CHARS}-char limit",
            file=sys.stderr,
        )
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("error: entry line must be a single line", file=sys.stderr)
        return 1
    encoded = LINE.encode("utf-8")
    if len(encoded) > MAX_CHARS:
        # The gate counts characters, but a byte cap keeps the entry
        # safely inside the limit even for multi-byte text.
        print(
            f"error: entry line is {len(encoded)} UTF-8 bytes, over the "
            f"{MAX_CHARS}-byte cap",
            file=sys.stderr,
        )
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(LINE)
    # Round-trip check: what the grader reads must be exactly the line.
    with open(out_path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != LINE:
        print("error: written entry differs from the entry line", file=sys.stderr)
        return 1
    print(f"wrote {len(LINE)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
