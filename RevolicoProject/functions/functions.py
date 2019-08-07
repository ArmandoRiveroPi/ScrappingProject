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

    Returns:
        float|int -- the average value
    """
    values = list(dic.values())
    average = sum(values)/len(values)
    return average


def dict_median(dic):
    """Calculates the median of the values in the dic

    Arguments:
        dic {dict} -- assumed to be a dictionary where the values are numbers

    Returns:
        float|int -- the median value
    """
    values = list(dic.values())
    values.sort()
    medianIndex = int(len(values)/2)
    median = values[medianIndex]
    return median
