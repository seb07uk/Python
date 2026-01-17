# echo.py
"""
Echo module written in pure Python.

This module provides:
- colored terminal output using ANSI escape codes,
- simple echo functionality,
- basic error handling.

The `run()` function is intended to be called automatically by the system,
while the `echo()` helper returns the provided text unchanged.

Author:
    Sebastian Januchowski

Contact:
    email:   polsoft.its@fastservice.com
    github:  https://github.com/seb07uk

Version:
    1.0.0 (2026-01-09)

License:
    MIT License
"""

# ANSI colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


def run(args=None):
    """
    Execute the echo command.

    Parameters
    ----------
    args : list[str] | None
        List of arguments passed to the command. If empty or None,
        a usage hint is displayed.

    Notes
    -----
    This function prints colored output directly to the terminal.
    """
    try:
        if not args:
            print(f"{YELLOW}Usage: e echo <text>{RESET}")
            return

        text = " ".join(args)
        print(f"{GREEN}{text}{RESET}")

    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")


def echo(text: str) -> str:
    """
    Return the provided text unchanged.

    Parameters
    ----------
    text : str
        The text to return.

    Returns
    -------
    str
        The same text that was passed in.
    """
    return text