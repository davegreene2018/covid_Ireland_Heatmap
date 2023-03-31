# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 19:29:48 2020

@author: Daveg
"""
# Purpose: prgram demonstaring the capabilites of the geopandas library by A00279700.

# import the required libaries
import matplotlib.pyplot as plt
#plt.rcParams.update({'figure.max_open_warning': 0}) # https://stackoverflow.com/questions/27476642/matplotlib-get-rid-of-max-open-warning-output
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# pip install pillow
import PIL
import io

def get_data_covid():
    
    """
    Function to process data 
    
    
    returns
    ----------
        mergeData : geopandas data frame
        
    
    """
    # import Irelands covid-19 stats
    data = pd.read_csv('Covid19CountyStatisticsHPSCIreland.csv')
    #data.sort_values('CountyName')
    # zip the lat and long and store them in a new column coordinates
    

    # remove columns we do not need from Covid19CountyStatisticsHPSCIreland.csv
    data = data.drop(columns = ['OBJECTID','ORIGID','PopulationCensus16','IGEasting','IGNorthing','UGI','PopulationProportionCovidCases',
                                'ConfirmedCovidDeaths','ConfirmedCovidRecovered','Shape__Area', 'Shape__Length'])
    
    
    #print(data.head())                      
    # Re-arrange the dataframe to show each date in a new column and county name as the index
    data = data.groupby([data.CountyName, 'TimeStamp'])['ConfirmedCovidCases'].first().unstack()
    

    # import the shape file for Ireland
    counties = gpd.read_file('All_Ireland_Shapefile/All_Ireland.shp')
    # remove columns we do not need
    counties = counties.drop(columns = ['OBJECTID', 'Brigade','Score_Test', 'Unit','ATCA', 'ATCP'])
    # drop counties from the north of Ireland
    counties = counties.drop([0,1,6,8,10,27])
    # check to make sure rows are dropped
    #print(counties.head()) 
    
    # check if counties in the shape file
#    for CountyName, row in data.iterrows():
#        if CountyName not in counties['COUNTY'].to_list():
#            print(CountyName,'not in list')
#        else:
#            pass
    
    
    # replace the name in the shape file with the name in the covid 19 csv file
    counties.replace("CO. CARLOW", "Carlow", inplace = True)
    counties.replace("CO. CAVAN", "Cavan", inplace = True)
    counties.replace("CO. CLARE", "Clare", inplace = True)
    counties.replace("CO. CORK", "Cork", inplace = True)
    counties.replace("CO. DONEGAL", "Donegal", inplace = True)
    counties.replace("CO. DUBLIN", "Dublin", inplace = True)
    counties.replace("CO. GALWAY", "Galway", inplace = True)
    counties.replace("CO. LAOIS", "Laois", inplace = True)
    counties.replace("CO. LOUTH", "Louth", inplace = True)
    counties.replace("CO. KILKENNY", "Kilkenny", inplace = True)
    counties.replace("CO. LONGFORD", "Longford", inplace = True)
    counties.replace("CO. KILDARE", "Kildare", inplace = True)
    counties.replace("CO. WICKLOW", "Wicklow", inplace = True)
    counties.replace("CO. WEXFORD", "Wexford", inplace = True)
    counties.replace("CO. OFFALY", "Offaly", inplace = True)
    counties.replace("CO. WESTMEATH", "Westmeath", inplace = True)
    counties.replace("CO. SLIGO", "Sligo", inplace = True)
    counties.replace("CO. WATERFORD", "Waterford", inplace = True)
    counties.replace("CO. MEATH", "Meath", inplace = True)
    counties.replace("CO. KERRY", "Kerry", inplace = True)
    counties.replace("CO. LEITRIM", "Leitrim", inplace = True)
    counties.replace("CO. LIMERICK", "Limerick", inplace = True)
    counties.replace("CO. MAYO", "Mayo", inplace = True)
    counties.replace("CO. MONAGHAN", "Monaghan", inplace = True)
    counties.replace("CO. ROSCOMMON", "Roscommon", inplace = True)
    counties.replace("CO. TIPPERARY", "Tipperary", inplace = True)
   
    
    
    
    # merge the data from counties with data on county name
    mergeData = counties.join(data, on = 'COUNTY', how = 'right')

    # return mergeData and data
    return mergeData, data, counties


def get_data_ireland():
    
    """
    Function to process geopandas data frame 
    
    
    returns
    ----------
        geodf : geopandas data frame containing lat and long of counties
        ireland : shape file of world countries
        
    
    
    """
    
    df = pd.DataFrame({
        'County': ['Carlow', 'Cavan', 'Clare', 'Cork', 'Donegal','Dublin', 'Galway', 'Kerry', 
                   'Kildare', 'Kilkenny','Laois', 'Leitrim', 'Limerick', 'Longford', 'Louth',
                   'Mayo', 'Meath', 'Monaghan', 'Offaly', 'Roscommon','Sligo', 'Tipperary', 
                   'Waterford', 'Westmeath', 'Wexford', 'Wicklow'],
        'Latitude': [52.7168,53.9878,52.8917,51.9517,54.8989,53.3605,53.3705,52.1689,53.238,52.5816,52.9952,54.1261,
                     52.5255,53.7325,53.9161,53.9191,53.6851,54.1857,53.2632,53.8008,54.1581,52.6407,52.2035,53.5524,52.5164,53.0205],
        'Longitude': [-6.8367,-7.2937,-8.9889,-8.6372,-7.96,-6.292,-8.7362,-9.565,-6.7837,-7.2175,-7.3423,-7.9939,-8.7412,
                      -7.6952,-6.487,-9.2537,-6.715,-6.9452,-7.6607,-8.2735,-8.5345,-7.9206,-7.4935,-7.4219,-6.5037,-6.3442]})
    
        
    df["Coordinates"] = list(zip(df.Longitude, df.Latitude))
    df["Coordinates"] = df["Coordinates"].apply(Point)
    
    
    
    geodf = gpd.GeoDataFrame(df, geometry="Coordinates")
    ireland = gpd.read_file('World_Countries/World_Countries.shp')
    
    return geodf, ireland

def show_county_lat_long(geodf, ireland):
    """
    Function to plot lat and long of counties in Ireland
    
    parameters
    ----------
        geodf : geopandas data frame
        ireland : shape file containing world countries
    
    
      
    """
    fig, gax = plt.subplots(figsize=(10,10))
    ireland.query("COUNTRY == 'Ireland'").plot(ax=gax, edgecolor='black', color='white')
    geodf.plot(ax=gax, color='red', alpha = 0.5)
    
    gax.set_xlabel('Longitude')
    gax.set_ylabel('Latitude')
    gax.set_title('Counties of Ireland')
      
    # Label the counties
    for x, y, label in zip(geodf['Coordinates'].x, geodf['Coordinates'].y, geodf['County']):
        gax.annotate(label, xy=(x,y), xytext=(4,4), textcoords='offset points')
    
    #img_lat_long = gax.get_figure()
    #return img_lat_long

def show_image(mergeData, select_date):
    """
    Function to plot covid-19 confirmed cases for a givin date by county
    
    parameters
    ----------
        mergeData : geopandas dataframe
        select_date : string containing date
    
    
    returns
    ----------
        img : figure containing status of each county for confirmed cases
        
    """
    
    ax = mergeData.plot(column = select_date+' 00:00:00+00', 
                        figsize = (15, 15),                        
                        legend = True,
                        cmap = 'OrRd',
                        scheme='user_defined', 
                        classification_kwds={'bins':[500, 1000, 2000, 3000, 4000, 5000, 7500, 10000, 20000, 30000]},
                        edgecolor = 'black',
                        linewidth = 0.9)
   
    ax.set_axis_off()
    ax.set_title(f'Total confirmed cases in Ireland for {select_date}', fontdict = {'fontsize':20}, pad =12.5)
    img = ax.get_figure()
    return img
    



def create_gif(date_from, date_to, file_name):
    """
    Function to generate confirmed cases by county for a date range
    
    parameters
    ----------
        date_from : string containing date from
        date_to : string containing date to
        filename : string 
    
        
    """
    # Create a list to store the images generated
    image_frames = []
    #dates = datetime
    date_from = date_from + ' 00:00:00+00'
    date_to = date_to + ' 00:00:00+00'
    date_from_index = mergeData.columns.get_loc(date_from)
    date_to_index = mergeData.columns.get_loc(date_to)
    
    for dates in mergeData.columns.to_list()[date_from_index:date_to_index]: #279
        
        
        ax = mergeData.plot(column = dates, 
                            figsize = (15, 15),                          
                            legend = True,
                            #legend_kwds={'label': "Total Confirmed Cases"},
                            cmap = 'OrRd', 
                            vmin = 0,
                            vmax = 22500,
                            edgecolor = 'black',
                            linewidth = 0.9)
        
        ax.set_axis_off()
        ax.set_title('Time Series of Covid-19 cases for Ireland '+ dates, fontdict = {'fontsize':20}, pad =12.5)
        img = ax.get_figure()
        
        f = io.BytesIO()
        img.savefig(f, format = 'png', bbox_inches= 'tight')
        f.seek(0)
        image_frames.append(PIL.Image.open(f))
        
    # save into a gif file
    image_frames[0].save(file_name+'.gif', format = 'GIF',
                append_images = image_frames[1:],
                save_all = True, duration = 300, loop = 1)
    # Close io bytes
    f.close()
    
    
    
# main program
if __name__ == "__main__":
    mergeData, data, counties = get_data_covid()
    geodf, ireland = get_data_ireland()
    
    while True:
        # prompt the user to enter a selection
        print("Program demonstrating geopandas library")
        choice = int(input("Select [1] for covid-19 data analysis or [2] to plot Lat, Long of counties [0] to exit "))
        if choice == 0:
            break
        elif choice == 1:
            print("Generate image for a givin date or gif image of date range")
            choice2 = int(input("Select [1] for confirmed cases by county or [2] to generate gif image"))
            if choice2 ==1:
                select_date = input('Input a date in the following format yyyy/mm/dd ')
                show_image(mergeData, select_date)
                break
            elif choice2 == 2:
                print("Minimun date range 2020/02/27")
                date_from = str(input('Input a date from in the following format yyyy/mm/dd '))
                print("Maximun date range 2020/12/01")
                date_to = str(input('Input a date to in the following format yyyy/mm/dd '))
                file_name = input('Enter a save name ')
                print("your gif file is been generated, please wait")
                create_gif(date_from, date_to, file_name)
                print(f"gif saved as {file_name} ")
                break
        elif choice == 2:
            print("Latitude and Longitude of counties in Ireland")
            show_county_lat_long(geodf, ireland)
            break
        
    
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
