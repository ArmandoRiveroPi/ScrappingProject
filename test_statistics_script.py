from RevolicoProject.Statistics import mean, median
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
    return classification.split(',')[0]


def get_prices_from_df(df, deviations=1000):
    strPrices = df['price'].tolist()
    prices = filter_prices(strPrices)
    prices = remove_outliers_robust(prices, deviations=deviations)
    return prices


dataFile = '/home/gauss/arm/importante/work/ai/projects/revolico/clean_data/ads_dump.csv'

df = pd.read_csv(dataFile)  # [0:10000]
df['classification'] = df['classification'].apply(
    lambda x: get_first_classification(x))

# GENERAL STATISTICS -------------
# strPrices = df['price'].tolist()
# prices = filter_prices(strPrices)
# prices = remove_outliers_robust(prices, deviations=1000)
prices = get_prices_from_df(df)
print('Prices Len', len(prices))
print_stats(prices)

# WORKING WITH GROUPS ----------------
groups = df.groupby('classification')
print('Groups', len(groups))
for group in groups:
    print('Group =============> ', group[0])
    prices = get_prices_from_df(group[1], deviations=100)
    print_stats(prices)
