"""
"""
import numpy as np
from scipy import stats


class ExploratoryStatistics(object):

    def get_statistics(self, vec):
        expStats = {
            # "position": {
            "N": len(vec),
            "mean": np.mean(vec),
            "median": np.median(vec),
            "q1": np.percentile(vec, 25),
            "q3": np.percentile(vec, 75),
            # },
            # "spread": {
            "range": np.ptp(vec),
            "variance": np.var(vec),
            "std": np.std(vec),
            "iqr": stats.iqr(vec),
            "mad": stats.median_absolute_deviation(vec),
            "cv": stats.variation(vec),
            "mad/median": stats.median_absolute_deviation(vec)/np.median(vec),
            "iqr/median": stats.iqr(vec)/np.median(vec),
            # },
            # "distribution": {
            # "log_histogram": np.histogram(np.log(vec))
            # }
        }
        for stat in expStats:
            expStats[stat] = round(expStats[stat], 2)
        return expStats

    def correlation_coefficients(self, matrix):
        pass
