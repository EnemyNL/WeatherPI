# WeatherPI

Collection of files required for my own twist to A raspberry weatherstation, based on the tutorial at: https://www.raspberryweather.com/

The getInfo.py python script is modified to include the following additions or alterations:
*More sensors:
  1x DHT 22 (temperature/humidity) sensor readout
  1x BME 280 (temperature/humidity/pressure) sensor readout
  1x DS18B20 (temperature) readout
*Limited (Max 30 loops) loop script to avoid readout issues on the DHT 22
*Checks to avoid the worst outlier readings. (Plan is to improve this to check against last readout, but this is not implemented yet.)
*Some alterations to database structure to include all readings
*Changed date and time storage to a single date-time value instead of split date and time. Purpose of this is to make charting better in the future, including custom selectable date/time ranges.


**How to**
To start using this, the following steps have to be taken:
*Follow tutorial as mentioned

*install dependencies for sensors in use
*alter database to include correct columns (DHT22_temp,DHT22_hum, BME280_temp, BME280_hum, BME280_press, DS18B20_temp, currentDateTime)
*alter database table to be named "WeatherData" (or change getInfo.py to use your preferred table name)
*open getInfo.py and find databaseUsername="YOUR USERNAME" and databasePassword="YOUR PASSWORD" . Replace with your database info

**To do**
*Update database creation script and include it here
*include sensor dependencies here
*create a better publication method instead of the one in the tutorial, which uses wordpress and a very limited range of data display (limitations include only being able to statically put up a graph for a specific date or "today", smoothed graphs, not being able to use the datetime format used in this altered version, not being able to include all sensor data as being created in this version).
