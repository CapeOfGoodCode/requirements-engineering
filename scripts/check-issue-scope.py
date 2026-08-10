#!/usr/bin/env python3
"""Warn -- never block -- when a commit message's scope has no issue reference.

Usage: check-issue-scope.py <commit-msg-file>
Exit code is always 0; this is a soft nudge, not a gate.
"""
import os
import re
import sys

SUBJECT = re.compile(r"^\w+(\(([^)]*)\))?(!)?:\s")


def warn(message):
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::warning::{message}")
    else:
        print(f"warning: {message}", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        print("usage: check-issue-scope.py <commit-msg-file>", file=sys.stderr)
        return 1

    with open(sys.argv[1], encoding="utf-8") as f:
        subject = f.readline().strip()

    match = SUBJECT.match(subject)
    if not match:
        return 0  # not Conventional-Commit shaped; commit-check's own check covers that

    scope = match.group(2)
    if not scope or not re.search(r"#\d+", scope):
        warn(
            "commit message has no issue reference in scope (e.g. 'feat(#12): ...') "
            "-- fine if this change isn't tied to a tracked issue"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
