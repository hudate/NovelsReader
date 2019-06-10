#!/user/bin/env python
#-*- coding -*-

import subprocess
import os

def getModules(moduleList):
    for needMoudle in moduleList:
        print('Module Name: %s'%needMoudle)
        try:
            __import__(needMoudle)
            print('You not need install module: %s'%needMoudle)
        except:
            print('You need to install module: %s'%needMoudle)
            if os.name=='nt':
                subprocess.call("python -m pip install "+ needMoudle, shell=True)
            elif os.name=='posix':
                subprocess.call("sudo python -m pip install " + needMoudle, shell=True)
            else:
                pass 
