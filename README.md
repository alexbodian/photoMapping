# photoMapping

The purpose of this application is to allow an investigator or any other person to have the ability to easily generate both a list of all the images in a directory with their timestamp, latitude, longitude, and the time zone of the image and then map all these image so that have a visual representation of the locations in which these images were taken.

In order to use this application, you first must have python 3.6 install on your environment as well as the following libraries:

dictionaries 
setuptools
folium
exifread
pandas
timezonefinder 
pytz

If you have installed all the libraries above and you are still missing the appropriate libraries to run the script the environment in which you are running the script should inform you of what additional libraries, you are lacking for the script. Also sometime if you get an error when installing the libraries on a unix environment you may have to use sudo to install the library.

To use the script, you must run the script from the same folder/directory of the photos you are trying to map. If you attempt to run the script and their either are no images within the folder or the images you have provided do not have any gps data the program will inform you of this and will not generate a map or timestamp text file. 

Assuming that you have a valid image or images within the folder then the program will proceed to list the information from the files in chronological order as well in the format of:

Index number of image in the list, filename, latitude, longitude, timezone

Additionally this information that is being output to the screen is also being written to file name timestamps.txt .

Next in the case that the user has more than 1 valid image in their folder the program will prompt the user to enter y or n for yes or no if they want to restrict the images that will be mapped depending on their date. This is included in the case that the user may only want to look at a certain day or set of days when looking at the map.

To indicate the dates in the case that the user had selected they will enter a range of values that correspond with the value that are next to the dates that were listed. Example:  0,1

In the case that the user wishes to only select 1 day from the list they can enter the same number twice separated by commas, (e.g. 1,1). 

Once the new dates are selected they will be shown in the terminal to indicate the new list of images that will be mapped.

The last option the user will have is the ability to indicate whether or not they want a line to be drawn between the points on the map that have been plotted. The purpose of this is to provide a visual indicator of the path someone may have travelled from the images that have been supplied. 

Based on the sample set of images that the user has supplied it may not make sense to enable this option since the line’s path may not make sense in terms of what it is presenting on the map.

Once the option of whether or not to have a line drawn is selected the map will be output to an index.html file and the entire image history list will be output to timestamps.txt. If the user chose the option to map a limited range of photos, the list of those details will be output to a file named timestamp_limited.txt.

Also note that the program tries to fit all the points in frame on first load, so if your data is grouped too far apart you may encounter some issues all the points being displayed in your zoom or location which may cause you to have to readjust your view on the map. Also depending on your zoom level some points may overlap if you zoomed out too far. You can fix this by zooming in more to get a precise view of the point’s locations’.


Please Note:	

Make sure you are running python 3.6 or you may encounter some errors that require you to run the script multiple times before it will execute properly.

