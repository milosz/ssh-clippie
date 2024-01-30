import errno
import os
import re

import click
import magic

from .definition import (
    permissions_definition_get_file,
    get_permissions_definition,
    display_file_types,
)
from .directory import get_ssh_directory
from .exit import set_exit_status
from .files import get_file_type, get_permissions
from .output import (
    print_message,
    print_header,
    print_error_message,
    print_error_message_with_fix,
)


def explain() -> None:
    """Parse permissions definition and explain applied checks"""

    permissions_definition = get_permissions_definition()

    # main directory
    print_header("Check main directory:")
    click.echo(
        f"Main directory should have permissions set to "
        f'{click.style(permissions_definition["ssh-clippie"]["main_directory"]["mode"], bold=True)}',
        nl=False,
    )
    main_directory_file_types = permissions_definition["ssh-clippie"]["main_directory"][
        "file_types"
    ]
    if main_directory_file_types:
        display_file_types(main_directory_file_types)
    click.echo()
    click.echo()

    # files
    print_header("Check configuration files:")
    for file in permissions_definition["ssh-clippie"]["files"]:
        click.echo(
            f'{click.style(file["name"], bold=True)} ({file["description"]}) {file["type"]}',
            nl=False,
        )
        click.echo(f' which is {click.style(file["condition"], bold=True)}', nl=False)
        if file["condition"] != "not expected":
            click.echo(
                f' and should have permissions set to {click.style(file["mode"], bold=True)}',
                nl=False,
            )
            if "file_types" in file:
                display_file_types(file["file_types"])
        click.echo()
    click.echo()

    # types
    print_header("Check configuration files types:")
    for _, file_type in permissions_definition["ssh-clippie"]["types"].items():
        click.echo(
            f'{click.style(file_type["name"], bold=True)} '
            f'matching file type "{click.style(file_type["pattern"], bold=True)}" '
            f'should have permissions set to {click.style(file_type["mode"], bold=True)}.'
        )
    click.echo()


def check_permissions_internal_directory(directory: str) -> None:
    """Parse permissions definition and perform checks"""
    permissions_definition = get_permissions_definition()

    item_file_path = os.path.join(directory)
    item_file_type = get_file_type(item_file_path)
    file_magic = None
    try:
        file_magic = magic.from_file(item_file_path, mime=False)
    except Exception as e:
        print_error_message(
            item_file_type, item_file_path, e.args[1], "should not exist"
        )
        set_exit_status(errno.EACCES)
        return
    for _, item_type in permissions_definition["ssh-clippie"]["types"].items():
        if re.match(item_type["pattern"], file_magic):
            break
    else:
        print_error_message(
            item_file_type, item_file_path, file_magic, "should not exists"
        )


def check_permissions() -> None:
    """Check permissions and display errors in verbose mode"""
    permissions_definition = get_permissions_definition()

    print_message(f"Checking {click.style(get_ssh_directory(), bold=True)} directory")
    print_message("")
    main_directory_item = permissions_definition["ssh-clippie"]["main_directory"]
    main_directory_path = os.path.join(get_ssh_directory())
    main_directory_permissions = get_permissions(main_directory_path)

    if main_directory_permissions != main_directory_item["mode"]:
        set_exit_status(errno.EACCES)
        print_error_message_with_fix(
            "Main directory",
            get_ssh_directory(),
            main_directory_permissions,
            main_directory_item["mode"],
        )

    for item_file in [
        f
        for f in get_permissions_definition()["ssh-clippie"]["files"]
        if f["condition"] == "mandatory"
    ]:
        item_path = os.path.join(get_ssh_directory(), item_file["name"])
        if not os.path.exists(item_path):
            set_exit_status(errno.ENOENT)
            print_message(
                f'{item_file["type"]} {click.style(item_path, bold=True)} does not exist'
            )

    for object_file in os.listdir(get_ssh_directory()):
        item_file = permissions_definition_get_file(object_file)
        if item_file:
            item_path = os.path.join(get_ssh_directory(), item_file["name"])
            if item_file["condition"] == "not expected":
                print_message(
                    f'{item_file["type"]} {click.style(item_path, bold=True)} should not exist'
                )
                set_exit_status(errno.ENOENT)
                continue
            try:
                path_permissions = get_permissions(item_path)
            except FileNotFoundError:
                set_exit_status(errno.ENOENT)
                print_message(
                    f'{item_file["type"]} {click.style(item_path, bold=True)} does not exist anymore'
                )
                continue

            if path_permissions != item_file["mode"]:
                set_exit_status(errno.EACCES)
                print_error_message_with_fix(
                    item_file["type"], item_path, path_permissions, item_file["mode"]
                )
            if item_file["type"] == "directory":
                for file in os.listdir(item_path):
                    check_permissions_internal_directory(
                        os.path.join(get_ssh_directory(), item_file["name"], file)
                    )
        else:
            check_permissions_internal_directory(
                os.path.join(get_ssh_directory(), object_file)
            )
