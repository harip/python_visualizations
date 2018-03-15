"""Average performance curve for each group"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PERF_DATA = pd.read_csv('timeseries.csv')

# Get distinct groups
GROUPS = PERF_DATA['Group'].unique()
GROUPS = sorted(GROUPS[~np.isnan(GROUPS)])

# Read column names and ignore Group column
COL_NAMES = [colname for colname in PERF_DATA.columns.values if "Age_" in colname]

PERF_AVGDATA_GROUPS = pd.DataFrame()
for group in GROUPS:
    group_values = PERF_DATA[PERF_DATA['Group'] == group]
    group_name = f'Group {int(group)}'
    group_means = [group_values[colname].mean() for colname in COL_NAMES]
    group_avg_values = pd.Series(group_means, name=group_name)
    PERF_AVGDATA_GROUPS = PERF_AVGDATA_GROUPS.append(group_avg_values)

PERF_AVGDATA_GROUPS.T.plot(ylim={0,100})
plt.show()
