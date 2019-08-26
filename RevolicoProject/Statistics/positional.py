"""Positional statistics describe a whole sample by
some measure of its location, like the average
"""
import numpy
import statistics

def mean(vect):
    return numpy.mean(vect)

def median(vect):
    return statistics.median(vect)