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


def dict_average(dic):
    """Returns the average of values contained in dic

    Arguments:
        dic {dict} -- assumed to be a dictionary where the values are numbers
    """
    values = list(dic.values())
    average = sum(values)/len(values)
    return average
