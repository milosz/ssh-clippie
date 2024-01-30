import os
from pathlib import Path


def get_file_type(path: str, follow: bool = True) -> str:
    """Determine file type for given path"""

    path_obj = Path(path)

    if Path.is_dir(path_obj):
        return "directory"
    # if Path.is_fifo(path_obj):
    #     return "fifo"
    # if Path.is_mount(path_obj):
    #     return "mount"
    if Path.is_socket(path_obj):
        return "socket"
    # if Path.is_block_device(path_obj):
    #     return "block_device"
    # if Path.is_char_device(path_obj):
    #     return "char_device"
    if Path.is_symlink(path_obj) and follow is True:
        destination = get_file_type(path, False)
        if destination != "unknown":
            return f"symlink to {destination}"
        return "broken symlink"
    if Path.is_file(path_obj):
        return "file"
    return "unknown"


def get_permissions(path: str) -> str:
    """Get permissions for given path"""
    file_mode = os.stat(path).st_mode
    file_permissions = oct(file_mode)[-3:]
    return file_permissions
