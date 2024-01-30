ssh_directory = ""


def set_ssh_directory(path: str) -> None:
    """Define global ssh directory"""
    global ssh_directory
    ssh_directory = path


def get_ssh_directory() -> str:
    """Get the global ssh directory"""
    global ssh_directory
    return ssh_directory
