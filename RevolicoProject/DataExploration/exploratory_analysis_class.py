""" This module carries the functionality for performing exploratory
analysis on the data.

The main feature of this type of analysis is that
you perform it on your whole data and you see all the results before
doing other more directed analysis, more adjusted to the particular dataset
you have.
"""

from .exploratory_visualization_class import ExploratoryVisualization
from .exploratory_statistics_class import ExploratoryStatistics
import pandas as pd


class ExploratoryAnalysis(object):
    """Encapsulates the exploratory analysis functionality
    """

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def build_(self, parameter_list):
        pass
