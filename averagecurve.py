"""Average performance curve"""

import pandas as pd
import matplotlib.pyplot as plt

PERF_DATA = pd.read_csv('timeseries.csv')

# Read column names
COL_NAMES = list(PERF_DATA.columns.values)

# get average values for each column as a series
AVG_VALUES = pd.Series([PERF_DATA[col_name].mean() for col_name in COL_NAMES])

# plot series
AVG_VALUES.plot(kind='line', grid=True, ylim={0, 100})
plt.show()
