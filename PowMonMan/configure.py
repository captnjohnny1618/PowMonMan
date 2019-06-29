import sys
import os
import yaml

#def checkForLocalConfig():
#
#    from pathlib import Path
#    user_home = str(Path.home())
#    
#    local_config_path = os.path.join(user_home,'.config','PowMonMan','rc.yaml')
#    if os.path.exists(local_config_path):
#        return local_config_path
#    else:
#        return os.path.join('PowMonMan','configs','rc.yaml')
    
def loadConfigurationFile(filepath = []):
    
    if not filepath:
        if (sys.platform=="linux" or sys.platform=="darwin"):
            filepath = os.path.join('/','var','local','PowMonMan','rc.yaml') #checkForLocalConfig()
        elif (sys.platform=="win32"):
            print("Windows support not yet implemented!")
            sys.exit(1)

    with open(filepath,'r') as f:
        configuration = yaml.load(f, Loader = yaml.FullLoader)
        
    return configuration 
