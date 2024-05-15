# import gpsd
# import os
# import asyncio


# # Connect to the local gpsd
# gpsd.connect()
# # Get gps position
# while(True):
# 	packet = gpsd.get_current()
# 	# See the inline docs for GpsResponse for the available data
# 	print(packet.position())

import serial
import pynmea2
from micropyGPS import MicropyGPS
ser = serial.Serial("/dev/ttyUSB1", 9600)
my_gps = MicropyGPS()
while True:
	nmea=str(ser.readline()).replace("b'", "").replace("\\r\\n'", "")
	for x in nmea:
		my_gps.update(x)
	print(my_gps.timestamp)
	print(my_gps.speed)
	print(my_gps.latitude)
	print(my_gps.longitude)