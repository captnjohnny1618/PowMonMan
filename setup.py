import sys
import os
import shutil
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from PowMonMan.filehandling import makeDirIfDoesntExist

class install(_install):
    linux_mac_dir = "/var/local/PowMonMan"
    linux_mac_filepath = os.path.join(linux_mac_dir,"rc.yaml")
    windows_path  = ""
    
    def run(self):
        _install.run(self)
        print("Installing config file...")
        makeDirIfDoesntExist('/var/local/PowMonMan/')
        if not os.path.isdir(self.linux_mac_dir):
            print("Could not save configuration file")
            sys.exit(1);
        try:
            shutil.copy("./PowMonMan/configs/rc.yaml", os.path.join(self.linux_mac_filepath))
        except IOError:
            print("WARNING: Configuration file was not installed (likely permissions issues)")
            sys.exit(1)
        print("Done!")

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
        "python-daemon>=1",
        "pyyaml>=5.1"
    ],
    
    packages = find_packages(),

    entry_points = {
        "console_scripts":[
            "powmonman_server = PowMonMan.PowMonMan_Server:main",
            "powmonman_client = PowMonMan.PowMonMan_Client:main"
        ]
    },    
    cmdclass={"install": install}
)
