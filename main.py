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
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    os.replace(tmp_path, path)


def validate_entry(text):
    """Gate: entry must be 1-200 chars, a single line, no leading/trailing
    whitespace, no double spaces. Fail loudly instead of shipping a bad entry."""
    if not 1 <= len(text) <= 200:
        raise SystemExit(
            f"entry gate failed: length rule violated — {len(text)} chars, must be 1-200"
        )
    if "\n" in text or "\r" in text:
        raise SystemExit(
            "entry gate failed: single-line rule violated — entry contains a newline character"
        )
    if text != text.strip():
        raise SystemExit(
            "entry gate failed: no-leading/trailing-whitespace rule violated"
        )
    if "  " in text:
        raise SystemExit("entry gate failed: no-double-space rule violated")


def main():
    validate_entry(LINE)
    write_entry(resolve_output_path(), LINE)
    try:
        repo_copy = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
        write_entry(repo_copy, LINE)
    except OSError:
        pass


if __name__ == "__main__":
    main()
