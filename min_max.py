import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import calendar as cl
from matplotlib.pyplot import figure, show, cm

def weather_pattern(file_name):
    df=pd.read_csv('data/C2A2_data/BinnedCsvs_d400/{}.csv'.format(file_name))
    df=df.drop(['ID'],axis=1)
    
    # Group by date, create seperate dataframes for tmin and tmax and merge 
    df_max1=df[df['Element']=="TMAX"].groupby(['Date','Element']).agg({'Data_Value':'max'}).reset_index()
    df_min2=df[df['Element']=="TMIN"].groupby(['Date','Element']).agg({'Data_Value':'min'}).reset_index()
    df=pd.concat([df_max1,df_min2]).reset_index()    
    
    # Create a pivot, tmax and tmin will become columns, split date in year,month,day
    # Determine the day of the year
    df= df.groupby(['Date', 'Element'])['Data_Value'].min().unstack('Element').reset_index() 
    df["TMAX"]=df["TMAX"]/10
    df["TMIN"]=df["TMIN"]/10
    df[["Year","Month","Day"]] =df["Date"].str.split("-",expand=True).astype('int')
    df["Day_Of_Year"]=(pd.to_datetime(df["Date"])).dt.dayofyear
    
    # Remove leap year data
    leap_df=df.query('Month ==2 & Day ==29')
    df=df.drop(leap_df.index.values)

    # Copy 2015 data into a dataframe, and years less than 2015 into another frame
    df_2015=df[df["Year"]==2015].reindex()
    df=df[df["Year"]<2015]
    df=df.drop(['Date','Year'],axis=1)

    # Merge df again based on day of the year
    df=df.groupby(['Day_Of_Year']).agg({'TMAX':'max','TMIN':'min'}).reset_index()

    # Get 2015 record breaking data
    df_record=pd.DataFrame(columns=['X','Y'])
    for k,v in df_2015.iterrows():
        # Get 2015 values for TMAX for this day and month
        tmax_value_2000_2014=df[(df["Day_Of_Year"]==v["Day_Of_Year"])]["TMAX"].values[0]
        tmin_value_2000_2014=df[(df["Day_Of_Year"]==v["Day_Of_Year"])]["TMIN"].values[0]

        if (v["TMAX"]>tmax_value_2000_2014):
            df_record.loc[len(df_record)]=[v["Day_Of_Year"],v["TMAX"]]

        if (v["TMIN"]<tmin_value_2000_2014):
            df_record.loc[len(df_record)]=[v["Day_Of_Year"],v["TMIN"]]      

    # Get x-tick positon at the change of the month (major ticks)
    # Get the minor ticks (middle of the month) and create labels as momths
    x_ticks=[ v[1]['Day_Of_Year'] for v in df_2015.iterrows() if v[1]['Day']==1 ]
    x_minor_ticks= [ (val+x_ticks[idx-1])/2 for idx,val in enumerate(x_ticks) if idx>0 ]
    x_minor_ticks.append( ( max(x_ticks)+365)/2 )
    x_minor_labels=[ month[:3] for month in cl.month_name if month!='' ]
    
    # Get the line series
    max_values=df['TMAX'].values
    min_values=df['TMIN'].values
    x_values=range(1,len(max_values)+1)

    # Plot the line data and apply a gradient to the entire chart
    FIG, AX = plt.subplots(nrows=1, ncols=1)
    FIG.canvas.draw()
    X = [ [.5, .5],[.6, .6]]
    AX.imshow(X, interpolation='bicubic', cmap=cm.copper,extent=(1, 365, -40, 50), alpha=1,aspect='auto')
    AX.plot(x_values,max_values,zorder=1,linewidth=0)
    AX.plot(x_values,min_values,zorder=1,linewidth=0)

    # Add the scatter plot
    scatter_colors=[ 1 for val in df_record["X"].values ]
    AX.scatter(df_record["X"].values,df_record["Y"].values,zorder=2, color='b',label="Record 2015 Temperature", alpha=0.75)
    AX.set_ylim([-40,50])
    AX.set_xlim([1,365])

    # Hide the major tick labels (ticks are visible)
    # Hide the minor ticks (tick labels which are months are visible)
    AX.tick_params(axis='x',length=0,which='minor')
    AX.tick_params(axis='y',which='major',labelsize=7.5)
    AX.set_xticks(x_ticks)
    AX.set_xticks(x_minor_ticks,minor=True)
    AX.set_xticklabels([])
    AX.set_xticklabels(x_minor_labels,minor=True, fontsize=7.5)

    # Set the grid and x,y labels, chart title and Scatter plot legend
    AX.grid(color='lightgrey',linewidth=0.5)
    plt.ylabel("Temperature (celsius)", fontsize=9)
    plt.title("Record high and low temperatures (2005-2014)", fontsize=12)
    plt.legend(loc=4,fontsize=6.5)

    # Fill area from the TMAX line to the top of chart with white color
    # Fill area from the TMIN line to the bottom of chart with white color
    # This will cause the gradient to showup only between the TMAX and TMIN
    max_y=[50 for min_value in min_values]
    min_y=[-40 for min_value in min_values]
    plt.fill_between(x_values,max_values,max_y,facecolor='white',alpha=1)
    plt.fill_between(x_values,min_values,min_y,facecolor='white',alpha=1)

    # Show the plot
    plt.show()

weather_pattern('fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')