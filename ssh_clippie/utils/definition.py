# from pathlib import Path

import click
import yaml

permissions_definition = {}


def load_permissions_definition(yaml_file: str) -> None:
    """Load permissions definition from yaml file"""
    global permissions_definition
    with open(yaml_file, "r") as file:
        permissions_definition = yaml.safe_load(file)


def get_permissions_definition() -> dict:
    """Get permissions_definition"""
    global permissions_definition
    return permissions_definition


def permissions_definition_get_file_type(file_type) -> dict:
    """Return specific file type by key"""
    global permissions_definition
    return permissions_definition["ssh-clippie"]["types"][file_type]


def permissions_definition_get_file(file) -> dict:
    """Return specific file by key"""
    global permissions_definition

    for element in permissions_definition["ssh-clippie"]["files"]:
        if element["name"] == file:
            return element
    else:
        return {}


def display_file_types(file_types: list) -> None:
    """Display file types names for keys"""
    global permissions_definition

    file_types_count = len(file_types)
    click.echo(f" and can contain", nl=False)
    for i, key in enumerate(file_types, start=1):
        click.echo(
            f' {click.style(permissions_definition_get_file_type(key)["name"], bold=True)}'
            f'{"," if i < file_types_count else "."}',
            nl=False,
        )
