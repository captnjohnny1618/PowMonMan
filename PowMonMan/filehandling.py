import sys
import os
from pathlib import Path

def makeDirIfDoesntExist(dirpath):
    try:
        os.mkdir(dirpath,mode = 0o644)
    except FileExistsError:
        pass
    except Exception as e:
        print("Could not make logging directory.  Are you sure you're running with root permissions?")
        sys.exit(1)

def makeFileIfDoesntExist(filepath):
    if not os.path.isfile(filepath):
        try:
            Path(filepath).touch()
        except Exception as e:
            print("Could not open logfile. Are you running with root permissions?")
            print(e)
            sys.exit(1)

def writePermissionsCheck(filepath):
    try:
        with open(filepath,'w') as f:
            f.write("Logfile check\n")
    except:
        print("Unable to write to logfile. Are you running with root permissions?")
        sys.exit(1)
