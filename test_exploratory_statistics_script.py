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
    return float(re.sub('[a-z,]', "", strPrice))


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
    return stData


def get_stats(rawData: pd.DataFrame, group='ALL'):
    stData = build_stats_df(rawData)
    Explorer = ExploratoryAnalysis(stData)
    stats = Explorer.all_column_stats(group)
    corr = Explorer.correlation_measures(group)
    return [stats, corr]


dataFile = '/home/gauss/arm/importante/work/ai/projects/revolico/clean_data/ads_dump1.csv'

df = pd.read_csv(dataFile)  # [0:1000]
df['classification'] = df['classification'].apply(get_first_classification)

stats, corr = get_stats(df)  # Explorer.all_column_stats()

groups = df.groupby('classification')
for count, group in enumerate(groups):
    groupDF = group[1]
    groupName = group[0]
    print(count, 'Group =============> ', groupName)
    groupStats, groupCorr = get_stats(groupDF, groupName)
    stats = pd.concat([stats, groupStats])
    corr = pd.concat([corr, groupCorr])

stats.to_csv('ExploratoryStats.csv')


# stData = build_stats_df(df)
# Explorer = ExploratoryAnalysis(stData)
# corr = Explorer.correlation_measures()
# print(corr)
corr.to_csv('Correlation.csv')
