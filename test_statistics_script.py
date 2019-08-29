# from RevolicoProject.Statistics import mean, median
from RevolicoProject.DataExploration import ExploratoryAnalysis
import numpy as np
from scipy import stats
import pandas as pd
import re
import math
import pprint


def remove_outliers(data):
    deviations = 3
    std = np.std(data)
    mean = np.mean(data)
    cleanData = [datum for datum in data if
                 abs(datum - mean) <= deviations * std]
    return cleanData


def remove_outliers_robust(data, deviations=10):
    iqr = stats.iqr(data)
    median = np.median(data)
    cleanData = [datum for datum in data if
                 abs(datum - median) <= deviations * iqr]
    return cleanData


def calculate_stats(data):
    return {
        # "position": {
        "mean": np.mean(data),
        "median": np.median(data),
        # },
        # "spread": {
        "range": np.ptp(data),
        "variance": np.var(data),
        "std": np.std(data),
        "iqr": stats.iqr(data),
        "mad": stats.median_absolute_deviation(data),
        "cv": stats.variation(data),
        # },
        # "distribution": {
        "log_histogram": np.histogram(np.log(data))
        # }
    }


def print_stats(data):
    statistics = calculate_stats(data)
    pprint.pprint(statistics, width=1)
    # print('Position -------')
    # print('Mean', np.mean(data))  # axis=1
    # print('Median', np.median(data))  # axis=1
    # # print('Percentile', np.percentile(data, 50))  # axis=1
    # print('Spread ---------')
    # print('Range', np.ptp(data))  # axis=1
    # print('Variance', np.var(data))  # axis=1
    # print('STD', np.std(data))  # axis=1
    # print('MAD', stats.median_absolute_deviation(data))  # axis=1
    # print('IQR', stats.iqr(data))  # axis=1
    # print('CV', stats.variation(data))  # axis=1
    # # print('Correlation', np.corrcoef(data))
    # print('Distribution ---')
    # print('Log Histogram', np.histogram(np.log(data)))


def filter_prices(strPrices):
    strPrices = [price for price in strPrices if isinstance(price, str)]
    prices = [float(re.sub('[a-z,]', "", price))
              for price in strPrices]
    prices = [price for price in prices if price > 0.0]
    return prices


def get_first_classification(classification: str):
    return classification.split(',')[0].strip(' >')


def get_prices_from_df(df, deviations=1000):
    strPrices = df['price'].tolist()
    prices = filter_prices(strPrices)
    prices = remove_outliers_robust(prices, deviations=deviations)
    return prices


def get_df_for_stats(rawData: pd.DataFrame):
    data = pd.DataFrame()
    data['price'] = rawData['price'].copy()
    data['time'] = rawData['datetime'].copy()
    return data


def recalculate_prices(strPrice):
    if not isinstance(strPrice, str):
        price = np.nan
    else:
        price = float(re.sub('[a-z,]', "", strPrice))
    return price


dataFile = '/home/gauss/arm/importante/work/ai/projects/revolico/clean_data/ads_dump1.csv'

df = pd.read_csv(dataFile)  # [0:10000]
df['classification'] = df['classification'].apply(
    lambda x: get_first_classification(x))


# GROUPS STATISTICS ----------------
groups = df.groupby('classification')
print('Groups', len(groups))
count = 1
groupStats = []
for count, group in enumerate(groups):
    # print(count, 'Group =============> ', group[0])
    prices = get_prices_from_df(group[1], deviations=100)
    data = pd.DataFrame({"prices": prices})
    Explorer = ExploratoryAnalysis(data)
    statistics = Explorer.column_statistics('prices')
    statistics['group'] = group[0]
    groupStats.append(statistics)
print_stats(prices)


# GENERAL STATISTICS -------------
# prices = get_prices_from_df(df)
# data = pd.DataFrame({"prices": prices})
data = pd.DataFrame()
data['prices'] = df['price'].copy()
data['prices'].apply(recalculate_prices)

Explorer = ExploratoryAnalysis(data)
statistics = Explorer.column_statistics('prices')
statistics['group'] = 'ALL'
groupStats.append(statistics)

# SAVE ALL THE STATISTICS ---------
results = pd.DataFrame(groupStats)
results.to_csv('ExpStats.csv')
print(results)
