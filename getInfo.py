#!/usr/bin/python
import sys
import Adafruit_DHT

import subprocess 
import re 
import os 
import glob
import time 
import MySQLdb as mdb 
import datetime
import bme280

databaseUsername="root"
databasePassword="am4408" 
databaseName="WeatherPI" #do not change unless you named the Wordpress database with some other name

sensor=Adafruit_DHT.DHT22 #if not using DHT22, replace with Adafruit_DHT.DHT11 or Adafruit_DHT.AM2302
pinNum=17 #if not using pin number 4, change here

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

DS18B20_temp = 0

def saveToDatabase(DHT22_temp,DHT22_hum,BME280_temp,BME280_hum,BME280_press,DS18B20_temp):

	con=mdb.connect("localhost", databaseUsername, databasePassword, databaseName)
        currentDateTime=datetime.datetime.now()

        now=datetime.datetime.now()
	
        with con:
                cur=con.cursor()
		
                cur.execute("INSERT INTO WeatherData (DHT22_temp,DHT22_hum, BME280_temp, BME280_hum, BME280_press, DS18B20_temp, currentDateTime) VALUES (%s,%s,%s,%s,%s,%s,%s)",(DHT22_temp,DHT22_hum,BME280_temp,BME280_hum,BME280_press,DS18B20_temp,currentDateTime))

		print "Saved temperature"
		return "true"


def readInfo():
	
	errorcounter = 0
	errorvar = 1
	
	DS18B20_temp = read_temp()
	DHT22_hum, DHT22_temp = Adafruit_DHT.read_retry(sensor, pinNum)#read_retry - retry getting temperatures for 15 times
	
	while errorvar >0 and errorcounter <30 :
		try: 
			BME280_temp, BME280_press, BME280_hum = bme280.readBME280All()
			errorvar = errorvar - 1
		except IOError:
			errorcounter = errorcounter + 1
			time.sleep(1)
			if errorcounter >29 :
				print "Max (30) loops reached. Script terminated."
				sys.exit()

	print "DHT 22 Temperature: %.1f C" % DHT22_temp
	print "DHT 22 Humidity:    %s %%" % DHT22_hum
	print "BME 280 Temperature: %.1f c" % BME280_temp
	print "BME 280 Humidity: %s %%" % BME280_hum
	print "BME 280 Pressure: %s" % BME280_press
	print "DS18B20 Temperature: %.1f c" % DS18B20_temp
	print "Amount of loops: %s " % errorcounter
	if DHT22_hum is not None and DHT22_temp is not None and not 0 <= DHT22_hum >= 100 and BME280_temp is not None and DHT22_temp-4 <= BME280_temp <= DHT22_temp+4:
		return saveToDatabase(DHT22_temp,DHT22_hum,BME280_temp,BME280_hum,BME280_press,DS18B20_temp) #success, save the readings
#       		 print 'klaar'
	else:
		print 'Failed to get reading. Try again!'
		readInfo()
		#sys.exit(1)

def read_temp_raw():
	catdata = subprocess.Popen(['cat',device_file], 
	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines

 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        DS18B20_temp = float(temp_string) / 1000.0
        return DS18B20_temp


#check if table is created or if we need to create one
try:
	queryFile=file("createTable.sql","r")

	con=mdb.connect("localhost", databaseUsername,databasePassword,databaseName)
        currentDate=datetime.datetime.now().date()

        with con:
		line=queryFile.readline()
		query=""
		while(line!=""):
			query+=line
			line=queryFile.readline()
		
		cur=con.cursor()
		cur.execute(query)	

        	#now rename the file, because we do not need to recreate the table everytime this script is run
		queryFile.close()
        	os.rename("createTable.sql","createTable.sql.bkp")
	

except IOError:
	pass #table has already been created
	

status=readInfo() #get the readings
