#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import requests
import json
import RPi.GPIO as GPIO

FLOAT_SENSOR = 23
PIR_SENSOR = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOAT_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIR_SENSOR, GPIO.IN)

while True:
    water_level = GPIO.input(FLOAT_SENSOR)
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    motion_detect = GPIO.input(PIR_SENSOR)

    data = {'humidity':humidity,'temperature':temperature,'water level':water_level, 'motion_detect': motion_detect}

    r = requests.get('http://farm-auto.herokuapp.com/api/post_reading?temperature=' + str(temperature) + '&humidity=' + str(humidity) + '&water_level=' + str(water_level) + '&motion_detect=' + str(motion_detect) + '&device_id=2143658709' )

    print(data)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    time.sleep(600)
