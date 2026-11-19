# Script to run all the programs and generate results.txt

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"
OUT = HERE.parent / "results.txt"
TIMEOUT = 30  # seconds per script per instance

SCRIPTS = {
    "A": HERE / "alternate.py",
    "F": HERE / "few.py",
    "M": HERE / "many.py",
    "N": HERE / "none.py",
    "S": HERE / "some.py",
}
COLS = ["A", "F", "M", "N", "S"]


def run_script(script, path):
    if not script.exists():
        return "N/A"
    try:
        with open(path) as f:
            p = subprocess.run(
                [sys.executable, str(script)],
                stdin=f, capture_output=True, text=True, timeout=TIMEOUT,
            )
    except subprocess.TimeoutExpired:
        return "?"
    out = p.stdout.strip()
    if p.returncode != 0 or not out:
        return "?"
    return out


def instance_size(path):
    with open(path) as f:
        return int(f.readline().split()[0])


def main():
    paths = sorted(DATA_DIR.glob("*.txt"))
    width = max(len(p.stem) for p in paths + [Path("Instance name")])

    rows = [["Instance name".ljust(width), "n"] + COLS]
    print("\t".join(rows[0]), file=sys.stderr)
    for path in paths:
        row = [path.stem.ljust(width), f"{instance_size(path):,}"]
        row += [run_script(SCRIPTS[c], path) for c in COLS]
        rows.append(row)
        print("\t".join(row), file=sys.stderr)

    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    line = "-" * 68
    with open(OUT, "w") as f:
        f.write(line + "\n\n")
        for row in rows:
            f.write("    ".join(c.ljust(w) for c, w in zip(row, widths)).rstrip() + "\n")
        f.write("\n" + line + "\n")


if __name__ == "__main__":
    main()