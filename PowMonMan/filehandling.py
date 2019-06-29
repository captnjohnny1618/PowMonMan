import sys
import os
from pathlib import Path
import stat

def makeDirIfDoesntExist(dirpath):
    try:
        os.mkdir(dirpath,mode = 0o755)
    except FileExistsError:
        pass
    except Exception as e:
        print("Could not make directory ({}).  Are you sure you're running with root permissions?".format(dirpath))
        sys.exit(1)

def makeFileIfDoesntExist(filepath):
    if not os.path.isfile(filepath):
        try:
            Path(filepath).touch()
            os.chmod(filepath,stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH) # (0644)
        except Exception as e:
            print("Could not open file ({}). Are you running with root permissions?".format(filepath))
            print(e)
            sys.exit(1)

def deleteFileIfExists(filepath):
    if os.path.isfile(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print("While trying to remove file {}, something went wrong.".format(filepath))
            print(e)
            sys.exit(1)
    

def writePermissionsCheck(filepath):
    try:
        with open(filepath,'w') as f:
            f.write("Logfile check\n")
    except:
        print("Unable to write to logfile. Are you running with root permissions?")
        sys.exit(1)
