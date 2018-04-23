#!/usr/bin/python3

import sys
import json
import time, datetime
import math
import paho.mqtt.client as mqtt
import signal
import secrets

def on_connect( client, userdata, flags, rc ):
  print( "Connected with code: " + str(rc) )
  client.subscribe("RF/data")

def on_message( client, userdata, msg ):
  try:  
    payload = json.loads(msg.payload.decode())

    print( payload )

    if 'rfin' in payload:
      payload = payload[ 'rfin' ]
      device  = payload[12:17]
      action  = payload[-1]

      # Bella's bedroom door
      if device == '60E90':
        topic    = 'home/upstairs/bellas_br/door'
        position = { 'E' : 'closed', 'A' : 'open' }.get( action, 'unknown' )
        data     = { 'position' :  position }
        jstring  = json.dumps( data )
        client.publish( topic, jstring )

      # Master bedroom motion
      if device == 'D2677':
        topic    = 'home/upstairs/master_br/motion'
        position = { 'E' : 'closed', 'A' : 'open' }.get( action, 'unknown' )
        data     = { 'position' :  position }
        jstring  = json.dumps( data )
        client.publish( topic, jstring )

  except:
      print( "Error processing packet" )

print("Starting up")
mqtt_broker = secrets.mqtt_broker

# Connect to MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect( mqtt_broker )
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.loop_forever()

