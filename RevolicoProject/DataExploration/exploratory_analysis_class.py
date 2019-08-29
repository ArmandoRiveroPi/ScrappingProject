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
        self.stats = ExploratoryStatistics()
        self.viz = ExploratoryVisualization()

    # ------- CLEANING SECTION -------------

    def clean(self):
        pass

    def remove_outliers(self):
        pass

    def fix_missing_data(self):
        pass

    # ----- STATISTICS SECTION ------
    def column_statistics(self, column):
        return self.stats.get_statistics(self.data[column])

    def all_column_stats(self, group='ALL'):
        stats = []
        cols = [str(col) for col in self.data.columns]
        for col in cols:
            statistics = self.column_statistics(col)
            statistics['variable'] = col
            statistics['group'] = group
            stats.append(statistics)
        return pd.DataFrame(stats)

    def correlation_measures(self, columns=None):
        pass
