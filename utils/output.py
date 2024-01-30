import click

verbose_mode = True


def set_verbose_mode(mode: str) -> None:
    """Define global verbose mode for each mode (verbose (true), quiet (false))"""
    global verbose_mode
    verbose_mode = True if mode == "verbose" else False


def get_verbose_mode() -> bool:
    """Get global verbose mode"""
    global verbose_mode
    return verbose_mode


def print_message(message: str) -> None:
    """Print message if verbose mode is enabled"""
    if get_verbose_mode():
        click.echo(message)


def print_header(message: str) -> None:
    """Print header if verbose mode is enabled"""
    if get_verbose_mode():
        click.echo(click.style(message, underline=True, bold=True))


def print_error_message(
    file_type: str, file_path: str, sub_message: str, message: str
) -> None:
    """Print error message for a file/directory"""
    print_message(
        f"{file_type} {click.style(file_path, bold=True)} ({click.style(sub_message, bold=True)}) {message}"
    )


def print_error_message_with_fix(
    file_type: str, file_path: str, current_value: str, expected_value: str
) -> None:
    """Print error message for a file/directory related to the used permissions with possible fix"""
    print_message(
        f"{file_type} {click.style(file_path, bold=True)} "
        f"permission are {click.style(current_value, bold=True)} "
        f"should be {click.style(expected_value, bold=True)}"
    )
