import sys

import click

from .output import print_message

exit_status = 0


def set_exit_status(exit_code: int) -> None:
    """Set exit status to specific exit code"""
    global exit_status
    exit_status = exit_code


def exit_application() -> None:
    """Exit application"""
    global exit_status
    if exit_status == 0:
        print_message(click.style("Success", fg="green"))
    else:
        print_message(click.style("Failed", fg="red"))
    sys.exit(exit_status)
