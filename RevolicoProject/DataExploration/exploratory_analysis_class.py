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
import numpy as np


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

    def correlation_measures(self, group='ALL'):
        methods = ['pearson', 'spearman', 'kendall']
        cols = [str(col) for i, col in enumerate(self.data.columns)]
        allCorr = pd.DataFrame()
        for ind, method in enumerate(methods):
            # Calculate the correlation
            correlation = self.data.corr(method=method)
            # Clean the autocorrelation to not see it later
            correlation.values[[np.arange(correlation.shape[0])]*2] = np.nan
            # Change the names in the index to concatenate without loosing data
            subDic = {col: col + "_" + method for col in cols}
            correlation.rename(index=subDic, inplace=True)
            # absSubDic = {col: col + "_" + 'abs' for col in cols}
            # absCorr = correlation.rename(columns=absSubDic).copy()
            # absCorr = absCorr.abs()
            # # correlation = pd.concat([correlation, absCorr])
            # correlation.reset_index().merge(absCorr, how="left",
            #                                 left_index=True).set_index('index')
            correlation = correlation.round(2)
            allCorr = pd.concat([allCorr, correlation])
        allCorr['group'] = group
        allCorr['N'] = self.data.shape[0]
        return allCorr
