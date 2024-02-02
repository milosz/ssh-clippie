from setuptools import setup
from setuptools import find_packages

setup(
    name="ssh-clippie",
    version="0.8.5",
    author="Milosz",
    author_email="milosz@sleeplessbeastie.eu",
    url="https://github.com/milosz/ssh-clippie",
    license="LICENSE",
    description="Small utility to check ssh client configuration (permissions and file types).",
    long_description=open('README.md').read(),
    install_requires=["click == 8.1.7", "python-magic == 0.4.27", "pyyaml == 6.0.1"],
    packages=["ssh_clippie", "ssh_clippie.utils"],
    package_data={"ssh_clippie":["permissions_definition.yaml"]},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ssh-clippie = ssh_clippie:cli",
        ],
    },
)
