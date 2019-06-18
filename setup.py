import os
import shutil
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

setup(
    name = "PowMonMan",
    version = "0.0.1",
    description = "Power monitoring and automated shutdown software",
    url = "https://github.com/captnjohnny1618/PowMonMan",
    license = "GNU GPL 2.0",

    long_description = "",
    author = "John Hoffman",
    keywords = "power monitor shutdown automated server client powmonman",
    platforms = ["Linux","Windows","MacOS"],
    install_requires = [
        "python-version>'3.0'",
        "python-daemon>=1"
    ],

    entry_points = {
        "console_scripts":[
            "powmonman_server = PowMonMan.PowMonMan_Server:main",
            "powmonman_client = PowMonMan.PowMonMan_Client:main"
        ]
    },

)
