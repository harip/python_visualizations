import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
import calendar as cl
from matplotlib.pyplot import figure, show, cm


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
    
    df_2015=df[df["Year"]==2015]
    df=df[df["Year"]<2015]

    # Max temperatures
    df_max=df[df['Element']=="TMAX"].groupby(['Month', 'Day','Element']).agg({'Data_Value':'max'}).reset_index()
    df_min=df[df['Element']=="TMIN"].groupby(['Month', 'Day','Element']).agg({'Data_Value':'min'}).reset_index()
    df=pd.concat([df_max,df_min]).reset_index()    

    # Create TMAX and TMIN columns and add day of the year column
    df= df.groupby(['Month', 'Day', 'Element'])['Data_Value'].min().unstack('Element')
    df.insert(0,"Day_Of_Year",range(1,len(df)+1))

    # Get 2015 record breaking data
    df_record=pd.DataFrame(columns=['X','Y'])
    for k,v in df.iterrows():
        # Get 2015 values for TMAX for this day and month
        tmax_values=df_2015[(df_2015["Day_Of_Year"]==v["Day_Of_Year"]) & (df_2015["Element"]=='TMAX')]["Data_Value"].values
        max_tmax_value=0 #max(tmax_values)

        # Get 2015 values for TMIN for this day and month
        tmin_values=df_2015[(df_2015["Day_Of_Year"]==v["Day_Of_Year"]) & (df_2015["Element"]=='TMIN')]["Data_Value"].values
        min_tmin_value=0 #min(tmin_values)

        if (max_tmax_value>v["TMAX"]):
            df_record.loc[len(df_record)]=[v["Day_Of_Year"],max_tmax_value]

        if (min_tmin_value<v["TMIN"]):
            df_record.loc[len(df_record)]=[v["Day_Of_Year"],min_tmin_value]        

    # Get x-tick positon at the change of the month
    x_ticks=[ v['Day_Of_Year'] for k,v in df.iterrows() if k[1]==1 ]
    x_minor_ticks= [ (val+x_ticks[idx-1])/2 for idx,val in enumerate(x_ticks) if idx>0 ]
    x_minor_ticks.append( ( max(x_ticks)+365)/2 )
    x_minor_labels=[ month[:3] for month in cl.month_name if month!='' ]
    
    # Get the line series
    max_values=df['TMAX'].values
    min_values=df['TMIN'].values
    x_values=range(1,len(max_values)+1)

    # plot
    FIG, AX = plt.subplots(nrows=1, ncols=1)
    FIG.canvas.draw()
    X = [ [.5, .5],[.6, .6]]
    AX.imshow(X, interpolation='bicubic', cmap=cm.copper,
    extent=(1, 365, -40, 50), alpha=1,aspect='auto')
    AX.plot(x_values,max_values,zorder=1,linewidth=0)
    AX.plot(x_values,min_values,zorder=1,linewidth=0)
    AX.scatter(df_record["X"].values,df_record["Y"].values,zorder=2,c='r',label="Record 2015 Temperature")
    AX.set_ylim([-40,50])
    AX.set_xlim([1,365])

    AX.tick_params(axis='x',length=0,which='minor')
    AX.tick_params(axis='y',which='major',labelsize=7.5)
    AX.set_xticks(x_ticks)
    AX.set_xticks(x_minor_ticks,minor=True)
    AX.set_xticklabels([])
    AX.set_xticklabels(x_minor_labels,minor=True, fontsize=7.5)

    AX.grid(color='lightgrey',linewidth=0.5)
    plt.ylabel("Temperature (celsius)", fontsize=9)
    plt.title("Record high and low temperatures (2005-2014)", fontsize=12)
    plt.legend(loc=4,fontsize=6.5)

    max_y=[50 for min_value in min_values]
    min_y=[-40 for min_value in min_values]

    plt.fill_between(x_values,max_values,max_y,facecolor='white',alpha=1)
    plt.fill_between(x_values,min_values,min_y,facecolor='white',alpha=1)

    plt.show()

# leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')
weather_pattern()