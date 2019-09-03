import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

sns.set(color_codes=True)

x = np.random.normal(size=100)
plot = sns.distplot(x)
plot.get_figure().savefig('histogram.jpg')
