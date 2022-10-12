# From a List of dictionnary retrieve a list of the element with key field of each dictionnary
def getFieldList(field,dictList):
    return [dict[field] for dict in dictList]


# From a List of List (listList) retrieve a list of the i-th element of each List
def getIndexList(i,listList, doAbs=False):
    if doAbs:
        return [abs(list[i]) for list in listList]
    else :
        return [list[i] for list in listList]