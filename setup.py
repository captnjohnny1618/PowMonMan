import os
import shutil
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install as _install


class install(_install):
    linux_mac_path = "/etc/PowMonMan/rc.yaml"
    windows_path  = ""
    
    def run(self):
        _install.run(self)
        print("Installing udev rules...")
        if not os.path.isdir("/etc/udev/rules.d"):
            print("WARNING: udev rules have not been installed (/etc/udev/rules.d is not a directory)")
            return
        try:
            shutil.copy("./rivalcfg/data/99-steelseries-rival.rules", "/etc/udev/rules.d/")
        except IOError:
            print("WARNING: udev rules have not been installed (permission denied)")
            return
        try:
            subprocess.call(["udevadm", "trigger"])
        except OSError:
            print("WARNING: unable to update udev rules, please run the 'udevadm trigger' command")
            return
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
        "python-version>'3.0'",
        "python-daemon>=1",
        "pyyaml>='5.1'"
    ],
    
    packages = find_packages(),

    data_files = [('PowMonMan/configs',["PowMonMan/configs/rc.yaml"])],

    entry_points = {
        "console_scripts":[
            "powmonman_server = PowMonMan.PowMonMan_Server:main",
            "powmonman_client = PowMonMan.PowMonMan_Client:main"
        ]
    },

)
