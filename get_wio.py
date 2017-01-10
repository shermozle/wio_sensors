#!/usr/bin/python

import urllib2
import json
import os
import time
import base64
import sys
from ISStreamer.Streamer import Streamer
import requests
import datetime

minutes_between_samples = 5

wio_server = "https://us.wio.seeed.io"

# Initial State bucket details
IS_BUCKET_NAME = "Wio python"
IS_BUCKET_KEY = os.environ['IS_BUCKET_KEY']
IS_ACCESS_KEY = os.environ['IS_ACCESS_KEY']
MYJSON_KEY    = os.environ['MYJSON_KEY']

# Initialize the Intial State streamer
streamer = Streamer(bucket_name=IS_BUCKET_NAME, bucket_key=IS_BUCKET_KEY, access_key=IS_ACCESS_KEY)

with open('wios.json', 'r') as f:
    wios = json.loads(f.read())


def get_reading(sensor, signal, token):
    api_reading_url = wio_server + sensor + "?access_token=" + token
    try:
        f = urllib2.urlopen(api_reading_url)
    except:
        print "Failed to get " + wio + ":" + signal
        return False
    reading = json.loads(f.read())
    f.close()
    return reading[signal]


def send_sparkfun(readings):
    try:
        url = 'https://data.sparkfun.com/input/XGyDJzNnozUQMw8Zd6z8?private_key=1JYBZeA8DeFEVdgPa4Yg&' + "&".join(
            readings)
        urllib2.urlopen(url)
    except:
        print("Error sending to sparkfun")

def send_myjson(readings):
    try:
        url = 'https://api.myjson.com/bins/' + MYJSON_KEY
        readings['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        requests.put(url, json=readings)
    except:
        print('Error sending to myjson.com')

def wio_sleep(token, minutes):
    try:
        url = 'https://us.wio.seeed.io/v1/node/pm/sleep/' + str(
            (minutes * 60) - 15) + '?access_token=' + token
        urllib2.urlopen(url, data="")
    except:
        print('Error sending upstairs to sleep')

while True:
    readings = {}
    readings_string = []
    for wio in wios:
        token = wios[wio]['token']
        for sensor in wios[wio]['sensors']:
            try:
                reading = str(get_reading(sensor['sensor'], sensor['signal'], token))
                this_sensor = wio + ":" + sensor['name']
                readings[this_sensor] = str(reading)
                readings_string.append(wio + sensor['name'] + "=" + str(reading))
                if this_sensor == 'downstairs:temperature':
                    inside = str(reading)
                if this_sensor == 'outside:temperature':
                    outside = str(reading)
                if this_sensor == 'outside:humidity':
                    humidity = str(reading)
                if this_sensor == 'upstairs:temperature':
                    upstairs = str(reading)
                if this_sensor == 'outside:light':
                    light = str(reading)
                if (reading != 'False'):
                    print(this_sensor + ": " + reading)
                    streamer.log(this_sensor, reading)
            except:
                print("Error")
                pass

        # Send it to sleep until we're ready to read it again
        if wios[wio]['sleep'] == True:
            wio_sleep(token, minutes_between_samples)

    send_sparkfun("=".join(readings_string))
    send_myjson(readings)
    print
    time.sleep(60 * minutes_between_samples)
