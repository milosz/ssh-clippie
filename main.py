#!/usr/bin/env python3

import os

import click

import utils


@click.command(no_args_is_help=True)
@click.option("--verbose", "mode", flag_value="verbose", help="Verbose mode")
@click.option("--quiet", "mode", flag_value="quiet", help="Quiet mode")
@click.option("--explain", "mode", flag_value="explain", help="Explain mode")
@click.option(
    "--ssh-directory",
    default=os.path.expanduser("~/.ssh"),
    type=click.Path(file_okay=False, dir_okay=True, exists=True, readable=True),
    show_default=True,
    help="Home directory",
)
@click.option(
    "--permissions-definition-file",
    default="permissions_definition.yaml",
    type=click.Path(file_okay=True, dir_okay=False, exists=True, readable=True),
    show_default=False,
    help="Permissions definition YAML file",
)
def cli(mode, ssh_directory, permissions_definition_file):
    """This script reads permissions definition from YAML file and performs checks against user ssh directory"""

    utils.set_verbose_mode(mode)
    utils.set_ssh_directory(ssh_directory)
    utils.load_permissions_definition(permissions_definition_file)

    if mode == "explain":
        utils.explain()
    else:
        utils.check_permissions()

    utils.exit_application()


if __name__ == "__main__":
    cli()
