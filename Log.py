from enum import Enum
from datetime import datetime
import os

class debugLvl(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

def debugLog(text,debugLvl):
    now = datetime.now()
    os.makedirs('./Log', exist_ok=True)
    if debugLvl == debugLvl.DEBUG:
        file = open('./Log/debug.txt', "a")
    elif debugLvl == debugLvl.INFO:
        file = open('./Log/info.txt', "a")
    elif debugLvl == debugLvl.WARNING:
        file = open('./Log/warning.txt', "a")
    elif debugLvl == debugLvl.ERROR:
        file = open('./Log/error.txt', "a")
    file.write('[' + str(now) + '] - ' + text + '\n')