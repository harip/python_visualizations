"""Average performance curve for each group"""

import pandas as pd
import matplotlib.pyplot as plt

PERF_DATA = pd.read_csv('timeseries.csv')
GROUP = 3
PERF_GROUP_DATA = PERF_DATA[PERF_DATA['Group'] == GROUP]

# Read column names and ignore Group column
COL_NAMES = [colname for colname in PERF_GROUP_DATA.columns.values if "Age_" in colname]

# Plot entire data set
GROUP_VALUES = PERF_GROUP_DATA.drop(columns=['Group']).T

# Get average for the group
GROUP_AVG_VALUES = pd.Series([PERF_GROUP_DATA[colname].mean() for colname in COL_NAMES])

plt.plot(range(len(COL_NAMES)), GROUP_VALUES, color='lightgray', linewidth=0.5)
plt.plot(GROUP_AVG_VALUES, color='black')
plt.show()
