import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
from collections import namedtuple

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
    val1=df[df['Element']=="TMAX"].groupby(['Date','Element']).max()
    val2=df[df['Element']=="TMIN"].groupby(['Date','Element']).min()

    val1=val1.add_suffix('_Max').reset_index()
    val2=val2.add_suffix('_Max').reset_index()

    val3=pd.concat([val1,val2])
    val4=val3.pivot(index='Date',columns='Element',values='Data_Value_Max')
    
    df_new=pd.DataFrame()
    df_new=val4

    print(df_new.columns.names())

    # indexed_df = val1.set_index(['Date'])
    #plt.subplots(nrows=1, ncols=1)
    
    # sr=pd.Series(val4["TMAX"])

    #plt.plot(df_new["Date"])
    
    #plt.show()
    
    #df1=val1.val3,columns='Element',values='Data_Value')

    # Creaval1year,month,day
    #df[["Year","Month","Day"]] =df["Date"].str.split("-",expand=True).astype('int')

    # Exclude leap year
    #leap_df=df.query('Month ==2 & Day ==29')
    #df=df.drop(leap_df.index.values)
    #print(df1)


# leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')
weather_pattern()