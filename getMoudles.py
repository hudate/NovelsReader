#!/user/bin/env python
#-*- coding -*-

import os
import time

def getModules(moduleList):
    for em in moduleList:
        while 1:
            try:
                __import__ em
                break
            except:
                os.system("python -m pip install " + em)
                sleep(0.2)

    



