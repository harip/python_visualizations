import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
import calendar as cl


def leaflet_plot_stations(binsize, hashid):
    df = pd.read_csv('BinSize_d{}.csv'.format(binsize))
    station_locations_by_hash = df[df['hash'] == hashid]
    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()
    plt.figure(figsize=(8,8))
    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)
    return mplleaflet.show()


def weather_pattern():
    df=pd.read_csv("fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv")
    df=df.drop(['ID'],axis=1)

    # Determine C,Day of Year
    df["Data_Value"]=df["Data_Value"]/10
    df[["Year","Month","Day"]] =df["Date"].str.split("-",expand=True).astype('int')
    df["Day_Of_Year"]=(pd.to_datetime(df["Date"])).dt.dayofyear

    # Remove leap year data
    leap_df=df.query('Month ==2 & Day ==29')
    df=df.drop(leap_df.index.values)

    # Max temperatures
    df_max=df[df['Element']=="TMAX"].groupby(['Month', 'Day','Element']).agg({'Data_Value':'max'}).reset_index()
    df_min=df[df['Element']=="TMIN"].groupby(['Month', 'Day','Element']).agg({'Data_Value':'min'}).reset_index()
    df=pd.concat([df_max,df_min]).reset_index()

    # Create TMAX and TMIN columns and add day of the year column
    df= df.groupby(['Month', 'Day', 'Element'])['Data_Value'].min().unstack('Element')
    df.insert(0,"DayOfYear",range(1,len(df)+1))
    
    # Get x-tick positon at the change of the month
    x_ticks=[ v['DayOfYear'] for k,v in df.iterrows() if k[1]==1 ]
    x_minor_ticks= [ (val+x_ticks[idx-1])/2 for idx,val in enumerate(x_ticks) if idx>0 ]
    x_minor_ticks.append( ( max(x_ticks)+365)/2 )
    x_minor_labels=[ month[:3] for month in cl.month_name if month!='' ]
 
    max_values=df['TMAX'].values
    min_values=df['TMIN'].values
    x_values=range(1,len(max_values)+1)

    # plot
    FIG, AX = plt.subplots(nrows=1, ncols=1)
    FIG.canvas.draw()
    AX.plot(x_values,max_values)
    AX.plot(x_values,min_values)
    AX.set_ylim([-40,50])
    AX.set_xlim([1,365])

    AX.tick_params(axis='x',length=0,which='minor')
    AX.set_xticks(x_ticks)
    AX.set_xticks(x_minor_ticks,minor=True)
    AX.set_xticklabels([])
    AX.set_xticklabels(x_minor_labels,minor=True)

    plt.fill_between(x_values,max_values,min_values)
    plt.show()

# leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')
weather_pattern()