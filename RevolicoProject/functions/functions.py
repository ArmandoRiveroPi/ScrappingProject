import json


def dict_unique(dicList):
    """Returns a list of dictionaries with duplicates removed

    Arguments:
        dicList {list} -- list of dictionaries to make unique

    Returns:
        list -- list of unique dictionaries
    """
    strList = [json.dumps(dic) for dic in dicList]
    strList = list(set(strList))
    uniqueDics = [json.loads(strRep) for strRep in strList]
    return uniqueDics
