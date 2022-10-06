from enum import Enum
from datetime import datetime

class debugLvl(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

def debugLog(text,debugLvl):
    now = datetime.now()
    if debugLvl == debugLvl.DEBUG:
        file = open('./debug.txt', "a")
    elif debugLvl == debugLvl.INFO:
        file = open('./info.txt', "a")
    elif debugLvl == debugLvl.WARNING:
        file = open('./warning.txt', "a")
    elif debugLvl == debugLvl.ERROR:
        file = open('./error.txt', "a")
    file.write('[' + str(now) + '] - ' + text + '\n')