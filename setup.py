import sys
import os
import shutil
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from PowMonMan.filehandling import makeDirIfDoesntExist

# Manually install the configuration files.  Unfortunately we have
# found too much inconsistency with how setuptools installs data_files
# or package files to rely on it as an adequate cross platform solution.
class install(_install):
    linux_mac_dir = "/var/local/PowMonMan"
    linux_mac_filepath = os.path.join(linux_mac_dir,"rc.yaml")
    windows_dir  = ""
    windows_filepath = ""
    
    def run(self):
        _install.run(self)
        print("Installing config file...")

        if ((sys.platform=="linux") or (sys.platform=="darwin")):
            dirpath  = self.linux_mac_dir
            filepath = self.linux_mac_filepath
        elif (sys.platform == "win32"):
            dirpath  = self.windows_dir
            filepath = self.windows_filepath
            print("Windows support is coming soon however not available just yet!")
            sys.exit(1)
        else:
            print("Looks like you're trying to install on an unsupported system!")
            print("We're defaulting to linux and mac path structures, but there's ")
            print("a good chance this won't work!  Consider requesting support for your")
            print("OS at https://github.com/captnjohnny1618/PowMonMan/issues. ")
            dirpath = linux_mac_dir
            filepath = linux_mac_filepath
            
        makeDirIfDoesntExist(dirpath)
        if not os.path.isdir(dirpath):
            print("Could not save configuration file")
            sys.exit(1);
        try:
            shutil.copy("./PowMonMan/configs/rc.yaml", filepath)
        except IOError:
            print("WARNING: Configuration file was not installed (likely permissions issues)")
            sys.exit(1)
        print("Done!")


# Detect the platform and configure dependencies if we're running on RPi
dependencies = [
    "python-daemon>=1",
    "pyyaml>=5.1"
]

if os.path.isfile('/sys/firmware/devicetree/base/model'):
    with open('/sys/firmware/devicetree/base/model','r') as f:
        s = f.read();
        if "Raspberry Pi" in s:
            dependencies.append("RPi.GPIO>=0.6.6")

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
    install_requires = dependencies,
    
    packages = find_packages(),

    entry_points = {
        "console_scripts":[
            "powmonman_server = PowMonMan.PowMonMan_Server:main",
            "powmonman_client = PowMonMan.PowMonMan_Client:main"
        ]
    },    
    cmdclass={"install": install}
)
