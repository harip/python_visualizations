"""Average performance curve with data distribution"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import pandas as pd

def get_distribution_box(xpos, parentbox, parentbox_xlim):
    """Function that returns the box where the histogram is placed"""

    xaxis_tick_width = (parentbox.x1-parentbox.x0)/parentbox_xlim
    hist_chart_x0 = (xpos*xaxis_tick_width)+parentbox.x0
    hist_chart_width = parentbox.x1+(xaxis_tick_width*xpos)
    return mtransforms.Bbox([[hist_chart_x0, parentbox.y0], [hist_chart_width, parentbox.y1]])

def get_distribution_chart(box, parent_yaxis, y_values, x_values, parent_xlim):
    """Function that returns histogram"""

    hist_chart = parent_yaxis.twiny()
    hist_chart.axis('off')
    hist_chart.set_xlim([0, parent_xlim])
    hist_chart.set_position(box)
    hist_chart.barh(y_values, x_values, align='center', color='lightgray', zorder=1)
    return hist_chart

PERF_DATA = pd.read_csv('https://res.cloudinary.com/harip/raw/upload/v1520830685/timeseries.csv')
GROUP = 3
PERF_GROUP_DATA = PERF_DATA[PERF_DATA['Group'] == GROUP]
COL_NAMES = [colname for colname in PERF_GROUP_DATA.columns.values if "Age_" in colname]
GROUP_AVG_VALUES = pd.Series([PERF_GROUP_DATA[colname].mean() for colname in COL_NAMES])
XLIM = 27
YLIM = 100

FIG, AX = plt.subplots(nrows=1, ncols=1)
PARENT_BOX = AX.get_position()

for idx, col_name in enumerate(COL_NAMES):
    age_data = PERF_GROUP_DATA[[col_name]].ix[:, 0].value_counts(sort=False).sort_index()
    age_data = age_data/age_data.max()
    y_pos = np.array([k for k, v in age_data.iteritems()])
    perf = np.array([v for k, v in age_data.iteritems()])
    distribution_box = get_distribution_box(idx, PARENT_BOX, XLIM)
    disChart = get_distribution_chart(distribution_box, AX, y_pos, perf, XLIM)

AVG = AX.twiny()
AVG.plot(GROUP_AVG_VALUES, color='black', zorder=2)
AX.set_ylim([0, YLIM])
AX.set_xlim([0, XLIM])
plt.show()
