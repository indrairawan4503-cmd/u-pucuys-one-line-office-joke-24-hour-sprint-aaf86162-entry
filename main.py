"""One-line office joke entry for make.fun.

Writes the entry to /output/entry.txt (or MAKEFUN_OUTPUT_DIR when set),
then best-effort to a repo-root entry.txt copy.
Deterministic: no network, no randomness, no time.
"""

import os

LINE = (
    "The meeting that should have been an email finally became one \u2014 "
    "it emailed itself, attended itself, took its own notes, and "
    "replied-all: 'You were optional. You always were.'"
)


def resolve_output_path():
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        if override.endswith(".txt"):
            return override
        return os.path.join(override, "entry.txt")
    return "/output/entry.txt"


def write_entry(path, text):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")


def main():
    write_entry(resolve_output_path(), LINE)
    try:
        repo_copy = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
        write_entry(repo_copy, LINE)
    except OSError:
        pass


if __name__ == "__main__":
    main()
