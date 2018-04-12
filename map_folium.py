#!/usr/bin/env python
'''
This script checks the directory that it is being run from
for any jpeg, jpg, or tiff files that have gpstags

It then outputs all the files in chronological order based on the date
and time of its creation while also taking the timezone fron it coordinates into account

It will then prompt the user for whether or not they want to limit the range of data that will be mapped
this is done by selecting the dates by the number in the list e.g. 1,2

After they do this they can then select whether or not they want to have a line drawn on the map that will
its best to draw the line based on the order in which points are plotted on the map

After this the an index.html file with points plotted will be generated as well a timestamps.txtfile that has
information from all the files in the format of timestamps_limited.txt will be generated if you restricted the 
range of photos.

Both timestamps.txt and timestamps_limited.txt will be generated with the following format:

     #   Timestamp                Filename      Latitude  Longitude  Timezone


'''


__author__ = 'Alex Bodian'
__date__ = '04-11-2018'
__version__ = '1.0'



from dictionaries import Dict, OrderedDict, FrozenDict, FrozenOrderedDict, ReadonlyDictProxy
import datetime
import folium
from folium.features import DivIcon
import sys
import os
import time
import string
import exifread
from folium import IFrame
from folium.plugins import MarkerCluster
from os import stat
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pandas as pd
from timezonefinder import TimezoneFinder
import pytz
from pytz import timezone, utc
from pytz.exceptions import UnknownTimeZoneError
import pandas as pd



def main():
    """The main function"""

if __name__ == '__main__':
    main()

date = []

# gps
loc = ''
exif_data = {}
lat_lon_tup = []
latitude = None
longitude = None
degrees = 0
minutes = 0
seconds = 0
longref = ''
latref = ''

coordListLat = []
coordListLon = []


# super-list
# datetime, filename, coordlistlat, coordlistlon, coordlistlatstr, coordliststrlonstr
temp_list = []
combined_list = []

for img in os.listdir('.'):
    if img.endswith('.jpeg') or img.endswith('.jpg') or img.endswith('.tiff'):
        cwd = os.getcwd()
        im = Image.open(img)
        exif = im._getexif()


        temp_list = []
        check = im._getexif()
        exif_data = {}


        f = open(img, 'rb')
        tags = exifread.process_file(f)
        for tag in tags.keys():
            if tag == 'GPS GPSLatitudeRef':
                latref = tags[tag]
                latref = latref.values[0] #type string

            if tag == 'GPS GPSLongitudeRef':
                longref = tags[tag]
                longref = longref.values[0] #type string

            if tag == 'GPS GPSLatitude' :

                '''
                This is mostly placeholder since it is generated based on system timezone info
                instead of the acutal timezone of where the picture was taken
                so this mainly just kept here since the values will be changed later
                on the loop
                '''

                # gets date and time in here since it's know to have gps coords
                time = os.path.getmtime(img)
                time_temp= time
                # date.append(datetime.datetime.fromtiddmestamp(time))
                time = datetime.datetime.fromtimestamp(time)
                time =  time.strftime('%Y-%m-%d')
                time = str(time)
                temp_list.append(time)
                time = os.path.getmtime(img)
                time = str(datetime.datetime.fromtimestamp(time))
                temp_list.append(time)


                # the name of the file is added to the list
                temp_list.append(img) #add filename

                latitude = tags[tag]
                
                degreesNum = (latitude.values[0].num)
                degreesDen = (latitude.values[0].den)
                degrees = (degreesNum/degreesDen)

                minutesNum = (latitude.values[1].num)
                minutesDen = (latitude.values[1].den)
                minutes = (minutesNum/minutesDen)

                secondsNum = (latitude.values[2].num)
                secondsDen = (latitude.values[2].den)
                seconds = (secondsNum/secondsDen)

                latitude = round(((seconds/3600) + (minutes/60) + degrees), 4)

            if tag == 'GPS GPSLongitude' :
                longitude = tags[tag]
                # converting d/m/s

                # http://pydoc.net/ExifRead/2.1.2/exifread.utils/

                # print(type(lat_temp))
                degreesNum = (longitude.values[0].num)
                degreesDen = (longitude.values[0].den)
                degrees = (degreesNum/degreesDen)

                minutesNum = (longitude.values[1].num)
                minutesDen = (longitude.values[1].den)
                minutes = (minutesNum/minutesDen)

                secondsNum = (longitude.values[2].num)
                secondsDen = (longitude.values[2].den)
                seconds = (secondsNum/secondsDen)

                longitude = round(((seconds/3600) + (minutes/60) + degrees), 4)

            if((latitude != None) and (longitude != None)):
                
                '''
                This is place where the coordinates will be modified accordingly based on the
                GPS reference variables in order to find the actual values for longitude and latitude
                '''
                if latref != 'N':
                            '''latitude = 0 - latitude'''
                            latitude = -(abs(0 - latitude))

                if longref != 'E':
                            '''longitude = 0 - longitude'''
                            longitude = -(abs(0 - longitude))


                lat_str = latitude
                lon_str = longitude

                tf = TimezoneFinder()

                timeZone = tf.timezone_at(lng= longitude, lat= latitude)



                
     
                # naive_datetime = time

                # tz = timezone(timeZone)
                # aware_datetime = naive_datetime.replace(tzinfo=tz)
                # aware_datetime_in_utc = aware_datetime.astimezone(utc)
                # naive_datetime_as_utc_converted_to_tz = tz.localize(timeZone)

                # timeZone = datetime(timeZone)




                # Makes it so that the times/dates for pictures 
                # set properly based on the timezone which is 
                # set based on the coordinates of the photo
                tz = pytz.timezone(timeZone)



                
                # gets date and time with proper timezone
                time = os.path.getmtime(img)
                time_temp= time
                # date.append(datetime.datetime.fromtiddmestamp(time))
                time = datetime.datetime.fromtimestamp(time, tz)
                time = time.strftime('%Y-%m-%d')
                time = str(time)
                temp_list[0] = time
    


                # 2018-04-04 09:06:00
                time = os.path.getmtime(img)
                time = (datetime.datetime.fromtimestamp(time, tz))
                time = time.strftime('%Y-%m-%d %H:%M:%S')
                time = str(time)
                temp_list[1] = time
                # print(time +' '+ timeZone)



                tup = (lat_str, lon_str)
                # print(type(tup))
                lat_lon_tup.append(tup)

                # coord = (lat_str, lon_str)
                coordListLat.append(lat_str)
                coordListLon.append(lon_str)

                temp_list.append(lat_str)
                temp_list.append(lon_str)

                y = "" + str(lat_str)
                z =  "" + str(lon_str)

                temp_list.append(y)
                temp_list.append(z)

                temp_list.append(timeZone)

                combined_list.append(temp_list)

                # reset variables
                loc = ''
                latitude = None
                longitude = None

















coordListLatStr = []
coordListLonStr = []
x = len(combined_list)

#if is here so that all the main code wont get run if there aren't any images with geotag info
if x != 0:

    combined_list.sort(key=lambda x: datetime.datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S"))

    # print(combined_list[])

    coordDict = {}
    dateDict = {}
    dateDict = OrderedDict(dateDict)
    




    i = len(combined_list)

    # Creating dictionary of coordinates
    for x in range(0, len(combined_list)):
        coordTup = (combined_list[x][3], combined_list[x][4])
        if coordTup in coordDict:
            update = coordDict[coordTup]       
            update.append(combined_list[x])
            coordDict[coordTup] = update

        else:
            coordDict[coordTup] = [] #creating empty list python
            update = coordDict[coordTup]       
            update.append(combined_list[x])
        

    # Creating dictionary of dates
    for x in range(0, i):
        date = combined_list[x][0]
        if date in dateDict:
            update = dateDict[date]       
            update.append(combined_list[x])
            dateDict[date] = update

        else:
            dateDict[date] = [] #creating empty list python
            update = dateDict[date]       
            update.append(combined_list[x])
            # dateList.append(date)

    



    # 0        1          2          3            4               5                 6               7
    #date datetime, filename, coordlistlat, coordlistlon, coordlistlatstr, coordliststrlonstr   timezone
    print("                                                                      ")
    print(" #   Timestamp                Filename             Latitude  Longitude  timezone")
    print("---------------------------------------------------------------------------------")
    print("                                                                      ")


    # Printing appropriate values for the header above
    for x in range(0, i):
        print('[', end= '')
        print(x, end= '] ')
        print(str(combined_list[x][1:5]) + ' ' + (combined_list[x][7]))

    print("                                                                      ")


    file = open('timestamps.txt', 'w')
    file.writelines(" #   Timestamp                Filename             Latitude  Longitude  timezone" + '\n')
    file.writelines("---------------------------------------------------------------------------------"+ '\n')
    file.writelines("                                                                      "+ '\n')

    for x in range(0, len(combined_list)):
        file.writelines('[' + str(x) +  ']')
        file.writelines(str(combined_list[x][1:5]) + ' ' + (combined_list[x][7])+ '\n')


    limited = False

    if len(combined_list) == 1:
        confirmation = 'n'
    else:
        confirmation = input("Do you want to limit the mapping of images by date? Enter y for yes or n for no: ")


    i = 0

    if (confirmation == 'y') or (confirmation == 'Y'):
        limited = True
        for key in dateDict.keys(): 
            print('[' + str(i) + '] ' , end= '')
            print (key)
            i = int(i)
            i = i + 1
        
        print("         ")
        date_start = input("Enter two numbers next to the dates and separate them by commas indicate the range of dates you want displayed: ")
        input_list = date_start.split(',')
        numbers = [int(x.strip()) for x in input_list]

        
        
        if ((numbers[0] > numbers[1]) or (numbers[0] < 0)  or (numbers[0] > len(dateDict))  or (numbers[1] > len(dateDict))):
            while True:
                print("Invalid values")
                print("         ")
                date_start = input("Enter two numbers next to the dates and separate them by commas indicate the range of dates you want displayed: ")
                input_list = date_start.split(',')
                numbers = [int(x.strip()) for x in input_list]

                # if ((date_start < (len(dateDict))) and   date_start >= 0 ):
                #         break


                if (numbers[0] > numbers[1]) and (numbers[1] < numbers[0]) and (numbers[0] >= 0) and (numbers < len(dateDict)):
                    break

                

        i = 0
        combined_list = []

        for key in dateDict:     
            
            if i >= numbers[0] and i <= numbers[1]:
                temporary = dateDict[key]
                length = (len(temporary))

                for x in range(0, length):
                    combined_list.append(temporary[x])
            i = i + 1


        # 0        1          2          3            4               5                 6               7
        #date datetime, filename, coordlistlat, coordlistlon, coordlistlatstr, coordliststrlonstr   timezone
        print("                                                                      ")
        print(" #   Timestamp                Filename             Latitude  Longitude  timezone")
        print("---------------------------------------------------------------------------------")
        print("                                                                      ")


        # Printing appropriate values for the header above
        for x in range(0, len(combined_list)):
            print('[', end= '')
            print(x, end= '] ')
            print(str(combined_list[x][1:5]) + ' ' + (combined_list[x][7]))


        print("                                                                      ")
        coordDict = {}
        dateDict = {}
        i = len(combined_list)


        file = open('timestamps_limited.txt', 'w')
        file.writelines(" #   Timestamp                Filename             Latitude  Longitude  timezone" + '\n')
        file.writelines("---------------------------------------------------------------------------------"+ '\n')
        file.writelines("                                                                      "+ '\n')

        for x in range(0, len(combined_list)):
            file.writelines('[' + str(x) +  ']')
            file.writelines(str(combined_list[x][1:5]) + ' ' + (combined_list[x][7])+ '\n')



        # Creating dictionary of coordinates
        for x in range(0, i):
            coordTup = (combined_list[x][3], combined_list[x][4])
            if coordTup in coordDict:
                update = coordDict[coordTup]       
                update.append(combined_list[x])
                coordDict[coordTup] = update

            else:
                coordDict[coordTup] = [] #creating empty list python
                update = coordDict[coordTup]       
                update.append(combined_list[x])
            

        # Creating dictionary of dates
        for x in range(0, i):
            date = combined_list[x][0]
            if date in dateDict:
                update = dateDict[date]       
                update.append(combined_list[x])
                dateDict[date] = update

            else:
                dateDict[date] = [] #creating empty list python
                update = dateDict[date]       
                update.append(combined_list[x])


        lat_lon_tup = []
        for j in range(0, len(combined_list)):
            tup = (combined_list[j][3], combined_list[j][4])
            lat_lon_tup.append(tup)




    # Finding the center coords

    latMax = -10000
    latMin = 10000

    lngMax = -10000
    lngMin = 10000


    latCen = 0
    lngCen = 0


    #  0     1 
    # lat , long
    for key in coordDict.keys(): 




        # lat extremes
        # max
        if key[0] > latMax:
            latMax = key[0]

        # min
        if key[0] < latMin:
            latMin = key[0]


        # long extremes
        # max
        if key[1] > lngMax:
            lngMax = key[1]

        # min
        if key[1] < lngMin:
            lngMin = key[1]

    

    
    latCen = (latMax + latMin)
    latCen = latCen/2
    lngCen = (lngMax + lngMin)
    lngCen = lngCen/2


    # 0        1          2          3            4               5                 6              7
    #date datetime, filename, coordlistlat, coordlistlon, coordlistlatstr, coordliststrlonstr  timezone
    # combined_list = []

    # https://leaflet-extras.github.io/leaflet-providers/preview/

    coords = []
    info = [] #list of descriptions
    placesAlreadyChecked = []
    internalVal = 0

    confirmation = input("Do you want a line to be drawn between the points that will be mapped? Enter y for yes or n for no: ")
    m = folium.Map(location=[latCen, lngCen],
    zoom_start=6,
    attr='&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    )

    if (confirmation == 'y') or (confirmation == 'Y'):
        folium.PolyLine(lat_lon_tup).add_to(m)



         
    for x in range(0, len(combined_list)):
        # use dict to check if more than 1 pic in that loc
        # use secondary list/dict to see if location was already checked so markers dont overlap
        coordTup = (combined_list[x][3], combined_list[x][4])
        
        if len(coordDict[coordTup]) ==  1:
            formatted = combined_list[x][2] + '<br>'+ "Latitude: " + combined_list[x][5] + '<br>' +"Longitutde: "+ combined_list[x][6] + "<br>" + combined_list[x][1]
            folium.map.Marker([combined_list[x][3],combined_list[x][4]],
            icon=DivIcon(
            icon_size=(15,15),
            icon_anchor=(0,0),
            html='<div>' +'<span style="color:#093145" font-weight:"bold" style="font-size: 50pt">' +'<h5>'+ '<b>' + str(internalVal)+ '<b>' +"</h5>" + '</span>''</div>',
            )
            ,popup='<i>'+ formatted +'</i>').add_to(m)
            internalVal = int(internalVal)
            internalVal +=1

        elif coordTup not in placesAlreadyChecked:
            formatted = ''
            temp = coordDict[coordTup]
            # print(len(temp))
            

            for j in range(0, len(temp)):
                formatted +=  temp[j][2] + '<br>'+ "Latitude: " + temp[j][5] + '<br>' +"Longitutde: "+ temp[j][6] + "<br>" + temp[j][1] + '<br>'+ '<br>'
            placesAlreadyChecked.append(coordTup)

            folium.map.Marker([combined_list[x][3],combined_list[x][4]],
            icon=DivIcon(
            icon_size=(15,15),
            icon_anchor=(0,0),
            html='<div>'+ '<span style="color:#093145" font-weight:"bold" style="font-size: 50pt">' +'<h5>' +'<b>'+str(internalVal)+ '<b>' +"</h5>" + '</span>' +'</div>',
            )
            ,popup='<i>'+ formatted +'</i>').add_to(m)
            internalVal = int(internalVal)
            internalVal +=1

    print("                                                                      ")

    if limited:
         # print("index.html with your mapped images and timestamps.txt with the timestamp info has been added to your folder ")
         print("index.html, timestamps.txt, and timestamps_limited.txt have been added to your folder")
    else:
         print("index.html and timestamps.txt have been added to your folder")

    
    
    m.save('index.html')
        
else:
    print("There are no images with geotag info in this folder so a map and timestamp report will not be generated.")
