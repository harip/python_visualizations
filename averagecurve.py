"""Average performance curve"""

import pandas as pd
import matplotlib.pyplot as plt

PERF_DATA = pd.read_csv('timeseries.csv')

# Read column names and ignore Group column
COL_NAMES = [colname for colname in PERF_DATA.columns.values if "Age_" in colname]

# get average values for each column as a series
AVG_VALUES = pd.Series([PERF_DATA[col_name].mean() for col_name in COL_NAMES])

# plot series
FIG, AX = plt.subplots(nrows=1, ncols=1)
FIG.set_size_inches(5.33,4)
AX.plot(AVG_VALUES, color='black', zorder=2)
AX.set_ylim([0, 100])
FIG.savefig('img/avgcurve.png',pad_inches=0,bbox_inches='tight')
plt.show()
