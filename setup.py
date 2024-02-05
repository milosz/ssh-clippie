from setuptools import setup

setup(
    name="ssh-clippie",
    version="0.8.1",
    py_modules=["main"],
    install_requires=["click == 8.1.7", "python-magic == 0.4.27", "pyyaml == 6.0.1"],
    entry_points={
        "console_scripts": [
            "ssh-clippie = main:cli",
        ],
    },
)
