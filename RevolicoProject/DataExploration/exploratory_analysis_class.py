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

    def __init__(self, groups: list):  # data: pd.DataFrame
        # Grouped data (name, DataFrame)
        self.groups = dict(list(groups))
        # self.data = data
        self.stats = ExploratoryStatistics()
        self.viz = ExploratoryVisualization()

    def set_groups(self, groups):
        self.groups = dict(list(groups))

    # ------- CLEANING SECTION -------------

    def clean(self):
        pass

    def remove_outliers(self):
        pass

    def fix_missing_data(self):
        pass

    # ----- STATISTICS SECTION ------
    def select_group(self, groupName):
        if groupName and groupName in self.groups:
            return self.groups[groupName]
        else:
            return None

    def column_statistics(self, column, groupName=""):
        data = self.select_group(groupName)
        return self.stats.get_statistics(data[column])

    def all_column_stats(self, group='ALL'):
        stats = []
        data = self.select_group(group)
        cols = [str(col) for col in data.columns]
        for col in cols:
            statistics = self.column_statistics(col, group)
            statistics['variable'] = col
            statistics['group'] = group
            stats.append(statistics)
        return pd.DataFrame(stats)

    def correlation_measures(self, group='ALL'):
        methods = ['pearson', 'spearman', 'kendall']
        data = self.select_group(group)
        cols = [str(col) for i, col in enumerate(data.columns)]
        allCorr = pd.DataFrame()
        for ind, method in enumerate(methods):
            # Calculate the correlation
            correlation = data.corr(method=method)
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
        allCorr['N'] = data.shape[0]
        return allCorr

    def get_stats(self, groupName):
        stats = self.all_column_stats(groupName)
        corr = self.correlation_measures(groupName)
        return [stats, corr]

    def groups_column_stats(self):
        stats = pd.DataFrame()
        corr = pd.DataFrame()
        for groupName in self.groups:
            # groupDF = group[1]
            print('Group =============> ', groupName)
            groupStats, groupCorr = self.get_stats(groupName)
            stats = pd.concat([stats, groupStats])
            corr = pd.concat([corr, groupCorr])
        return [stats, corr]

    # ----- VISUALIZATION SECTION -----
