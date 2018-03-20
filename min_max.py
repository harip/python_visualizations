"""Coursera data science course"""

import calendar as cl
import matplotlib.pyplot as plt
import pandas as pd

DATA_URL = "https://res.cloudinary.com/harip/raw/upload/v1521364790/site/python/minmax.csv"
XLIM=[1, 365]
YLIM=[-40, 50]

def prep_initial_data():
    """Drop unused column and group by columns"""
    df_main = pd.read_csv(DATA_URL)
    df_main = df_main.drop(['ID'], axis=1)
    # Group by date,  create seperate dataframes for tmin and tmax and merge
    groupby_fields = ['Date', 'Element']
    df_max1 = df_main[df_main['Element'] == "TMAX"].groupby(groupby_fields).agg({'Data_Value':'max'}).reset_index()
    df_min2 = df_main[df_main['Element'] == "TMIN"].groupby(groupby_fields).agg({'Data_Value':'min'}).reset_index()
    df_main = pd.concat([df_max1, df_min2]).reset_index()
    return df_main

def basic_chart_settings(chart_plot):
    """Basic chart settings"""
    chart_plot.imshow([[.5, .5], [.6, .6]], interpolation='bicubic', cmap=plt.cm.copper, extent=(1, 365, -40, 50), alpha=1, aspect='auto')

    # Basic chart settings
    chart_plot.set_xticklabels([])
    chart_plot.set_ylim(YLIM)
    chart_plot.set_xlim(XLIM)
    chart_plot.tick_params(axis='x', length=0, which='minor')
    chart_plot.tick_params(axis='y', which='major', labelsize=7.5)

    # Set the grid and x, y labels,  chart title and Scatter plot legend
    chart_plot.grid(color='lightgrey', linewidth=0.5)
    plt.ylabel("Temperature (celsius)", fontsize=9)
    plt.title("Record high and low temperatures (2005-2014)", fontsize=12)
    plt.legend(loc=4, fontsize=6.5)

def weather_pattern():
    """Function that creates the chart"""
    df_main = prep_initial_data()    

    # Create a pivot,  tmax and tmin will become columns,  split date in year, month, day
    # Determine the day of the year
    df_main = df_main.groupby(['Date', 'Element'])['Data_Value'].min().unstack('Element').reset_index()
    df_main["TMAX"] = df_main["TMAX"]/10
    df_main["TMIN"] = df_main["TMIN"]/10
    df_main[["Year", "Month", "Day"]] = df_main["Date"].str.split("-", expand=True).astype('int')
    df_main["Day_Of_Year"] = (pd.to_datetime(df_main["Date"])).dt.dayofyear

    # Remove leap year data
    leap_df = df_main.query('Month  == 2 & Day  == 29')
    df_main = df_main.drop(leap_df.index.values)

    # Copy 2015 data into a dataframe,  and years less than 2015 into another frame
    df_2015 = df_main[df_main["Year"] == 2015].reindex()
    df_main = df_main[df_main["Year"] < 2015]
    df_main = df_main.drop(['Date', 'Year'], axis=1)

    # Merge df again based on day of the year
    df_main = df_main.groupby(['Day_Of_Year']).agg({'TMAX':'max', 'TMIN':'min'}).reset_index()

    # Get 2015 record breaking data
    df_record = pd.DataFrame(columns=['X', 'Y'])
    for k, row_val in df_2015.iterrows():
        # Get 2015 values for TMAX for this day and month
        tmax_value_2000_2014 = df_main[(df_main["Day_Of_Year"] == row_val["Day_Of_Year"])]["TMAX"].values[0]
        tmin_value_2000_2014 = df_main[(df_main["Day_Of_Year"] == row_val["Day_Of_Year"])]["TMIN"].values[0]

        if row_val["TMAX"] > tmax_value_2000_2014:
            df_record.loc[len(df_record)] = [row_val["Day_Of_Year"], row_val["TMAX"]]

        if row_val["TMIN"] < tmin_value_2000_2014:
            df_record.loc[len(df_record)] = [row_val["Day_Of_Year"], row_val["TMIN"]]

    # Get x-tick positon at the change of the month (major ticks)
    # Get the minor ticks (middle of the month) and create labels as momths
    x_ticks = [row_val[1]['Day_Of_Year'] for row_val in df_2015.iterrows() if row_val[1]['Day'] == 1]
    x_minor_ticks = [(val+x_ticks[idx-1])/2 for idx, val in enumerate(x_ticks) if idx > 0]
    x_minor_ticks.append((max(x_ticks)+365)/2)
    x_minor_labels = [month[:3] for month in cl.month_name if month != '']

    # Get the line series
    max_values = df_main['TMAX'].values
    min_values = df_main['TMIN'].values
    x_values = range(1, len(max_values)+1)

    # Plot the line data and apply a gradient to the entire chart
    chart_fig, chart_plot = plt.subplots(nrows=1, ncols=1)
    chart_fig.canvas.draw()
     
    chart_plot.plot(x_values, max_values, zorder=1, linewidth=0)
    chart_plot.plot(x_values, min_values, zorder=1, linewidth=0)

    # Add the scatter plot
    chart_plot.scatter(df_record["X"].values, df_record["Y"].values, zorder=2, color='b', label="Record 2015 Temperature", alpha=0.75)

    # Hide the major tick labels (ticks are visible)
    # Hide the minor ticks (tick labels which are months are visible)     
    chart_plot.set_xticklabels(x_minor_labels, minor=True, fontsize=7.5)
    chart_plot.set_xticks(x_ticks)
    chart_plot.set_xticks(x_minor_ticks, minor=True)
    basic_chart_settings(chart_plot)  
    
    # Fill area from the TMAX line to the top of chart with white color
    # Fill area from the TMIN line to the bottom of chart with white color
    # This will cause the gradient to showup only between the TMAX and TMIN
    max_y = [50 for min_value in min_values]
    min_y = [-40 for min_value in min_values]
    plt.fill_between(x_values, max_values, max_y, facecolor='white', alpha=1)
    plt.fill_between(x_values, min_values, min_y, facecolor='white', alpha=1)

    # Show the plot
    plt.show()

weather_pattern()
