from RevolicoProject.DataExploration import ExploratoryAnalysis
import numpy as np
from scipy import stats
import pandas as pd
import re
import math
import pprint
import dateutil.parser
import datetime


def get_first_classification(classification: str):
    return classification.split(',')[0].strip(' >')


def recalculate_prices(strPrice):
    return math.log10(float(re.sub('[a-z,]', "", strPrice)))


def recalculate_time(dtStr: str):
    dateTime = dateutil.parser.parse(dtStr)
    return dateTime.hour


def recalculate_weekday(dtStr: str):
    dateTime = dateutil.parser.parse(dtStr)
    return dateTime.weekday()


def build_stats_df(rawDF: pd.DataFrame):
    stData = pd.DataFrame()
    # Copy columns from raw data
    stData['price'] = rawDF['price'].copy()
    stData['hour'] = rawDF['datetime'].copy()
    stData['weekday'] = rawDF['datetime'].copy()
    # Drop rows with missing data
    stData.dropna(inplace=True)
    # Transform the columns to have the numeric values we want
    stData['price'] = stData['price'].apply(recalculate_prices)
    stData['hour'] = stData['hour'].apply(recalculate_time)
    stData['weekday'] = stData['weekday'].apply(recalculate_weekday)
    stData = remove_outliers(stData)
    return stData


def remove_outliers(df, deviations=10):
    # List of bools telling whether to keep the row
    keep = [True for i in range(df.shape[0])]
    # Loop through all the columns
    for column in df.columns:
        col = str(column)
        # Find the median and the iqr for the column
        colData = df[col]
        median = np.median(colData)
        iqr = stats.iqr(colData)
        # Loop through the values for the column
        row = 0
        for value in colData:
            # If the value is outside median+-(deviations)*iqr
            # mark the row with False to be deleted
            if abs(value - median) > deviations * iqr:
                keep[row] = False
            row += 1

    # Filter the df with the bool list
    toKeep = pd.Series(keep, index=df.index)
    newDF = df[toKeep]
    return newDF


def get_stats(rawData: pd.DataFrame, group='ALL'):
    stData = build_stats_df(rawData)
    Explorer = ExploratoryAnalysis(stData)
    stats = Explorer.all_column_stats(group)
    corr = Explorer.correlation_measures(group)
    return [stats, corr]


dataFile = '/home/gauss/arm/importante/work/ai/projects/revolico/clean_data/ads_dump1.csv'

df = pd.read_csv(dataFile)  # [0:1000]
df['classification'] = df['classification'].apply(get_first_classification)


groups = df.groupby('classification')
groups = [(group[0], build_stats_df(group[1])) for group in groups]
statsDF = build_stats_df(df)
groups.append(("ALL", statsDF))
exp = ExploratoryAnalysis(groups)
# exp.set_groups(groups)

exp.group_box_plot()
exp.viz.pair_plot(statsDF)
# stats, corr = exp.groups_column_stats()
# stats.to_csv('ExploratoryStats.csv')
# corr.to_csv('Correlation.csv')
