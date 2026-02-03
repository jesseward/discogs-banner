import os
from setuptools import setup, find_packages

NAME = "discogs-banner"
VERSION = "2.1.0"

setup(
    name=NAME,
    version=VERSION,
    author="Jesse Ward",
    author_email="jesse@jesseward.com",
    description=(
        "Creates an image banner from the album thumbnails in your Discogs collection."
    ),
    license="MIT",
    url="https://github.com/jesseward/discogs-banner",
    scripts=["scripts/discogs-banner.py"],
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "discogs_client",
        "requests",
    ],
    data_files=[
        (
            os.path.expanduser("~/.config/{0}".format(NAME)),
            ["config/discogs-banner.conf"],
        )
    ],
)
