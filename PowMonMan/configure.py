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
    
def loadConfigurationFile():

    filepath = os.path.join('PowMonMan','configs','rc.yaml') #checkForLocalConfig()
    
    with open(filepath,'r') as f:
        configuration = yaml.load(f, Loader = yaml.FullLoader)
        
    return configuration 
