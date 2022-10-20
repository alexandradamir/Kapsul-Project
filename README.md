# Kapsul-Project
### Cleaning function
I created a [cleaning function](https://github.com/alexandradamir/Kapsul-Project/blob/main/cleaning_function.py) that should work on all datasets. This function creates an id column, that starts from 1, if there is none, cleaned the columns name from Turkish characters and standardize them as "snake_case" , change every date format to ISO8601 date format and every number format to the right format. (ex: 1234567.89). 
The number and date format function finds every possible format and converts it to standard format. For this reason, this script could be used for any data set in the future.  
The number cleaning function could be improved, currently the function loops through every value in every column and this could be too long of a process for larger datasets. The function could be improved if you loop just through the columns as in date cleaning function. 
### Dashboard
I also developed a [dashboard](https://github.com/alexandradamir/Kapsul-Project/blob/main/dashboard.py) based on open data about air quality measurement stations around Konya. I used both geospatial and numerical data to create a dashboard with a map view and other features. Location of the air quality stations appear on the map and detailed information is provided for each station when clicked. Air quality and other sensor data is matched to have a better dashboard. 
When the air quality station is clicked, on the right side, information like name of the station clicked, last date registered and the air quality measures for that date appear. 
Below the map, when a station is clicked, a date picker, 2 drop-down menus and a graph appear. Using these elements, the user can customize different graphs of interest. With the help of the date selector, the user can select the exact period for which he wants to see the chart. The air quality measure and the graph type can also be chosen. There are 3 types of graphs available, the trend over time, the comparison between days and the comparison between months. 
For [data cleaning](https://github.com/alexandradamir/Kapsul-Project/blob/main/datasets_cleaning.py) I used the function I previously developed. In addition, for the geographic information dataset with the station points. I formatted the latitude and longitude and converted the data frame to geographic data frame and replaced the Turkish letters in the stations name.  
At first, I created in the body of the app with the map and its points, a title for the dashboard, a place to store the data so it can be shared between callbacks and a container for each element that appears when a station point is clicked. 
I created a callback to store the database and other callbacks to display different elements on the dashboard. 
Firstly, when a point is clicked the dataset for that point is stored to be used in the future callbacks. If no point has been selected a message will appear indicating to press a point on the map. After a point is clicked, a series of chained callbacks are triggered creating the dashboard. The information about that point and the graph for one of the measures appear, as well as options that the user can select from to create a custom graph based on their interest. 
This was just a test code, so not all stations information is available, but they can be easily added to the code, just repeat the code as for the other two available datasets. 
It could be useful if on the right-side information, the user can change the date to see information about days other than the last registered one. Also, the chart trend for days might get a bit crowded, so it could be helpful if the user can only select a few days for that particular chart type. It will be more visually pleasing if on the map the points are labeled from the start so the user knows which point is which station. 
