#!/usr/bin/env python3

import sys

from myproject.utils.django import run_django_management


def print_notice():
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        return
    print("WARNING: No specific site is loaded.", file=sys.stderr)
    print(
        "Run `python -m myproject.sites.SITE_NAME` to manage a specific site.",
        file=sys.stderr,
    )
    print("You should only use this script for tests and linting.", file=sys.stderr)
    if len(sys.argv) == 2 and sys.argv[1] == "runserver":
        print(
            "To run the server, use `python -m myproject.sites.SITE_NAME`.",
            file=sys.stderr,
        )
        exit(1)


if __name__ == "__main__":
    try:
        print_notice()
        run_django_management("myproject.settings._linter_settings")
    finally:
        print_notice()
