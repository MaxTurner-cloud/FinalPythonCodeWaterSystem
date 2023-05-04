# This program takes the data (Temperature, Pressure, and Relative Humidity) from the Atmospheric Breakout sensor,
# scales it, tags it then sends it to the EmonHub running on the basePi. the username and password because those are
# built into the Emonpi.

from __future__ import print_function
import paho.mqtt.publish as publish
import qwiic_bme280
import sys
import datetime
import time

HostIP = "172.30.168.126"   # This is the IP of the BasePi running the Emon server
mySensor = qwiic_bme280.QwiicBme280()
mySensor.begin()  # start atm breakout sensor
sleepTime = 20  # time between data grabs
sprinklerName = "Sprinkler1"    # which sprinker is it mounted to

if mySensor.connected:
    hum_scaled = (float(mySensor.humidity) / 0.414)
    humidity = (str(hum_scaled))  # find humidity
    atm_scaled = (float(mySensor.pressure) / 146.45)  # convert from pa to millibar
    atm_pressure = (str(atm_scaled))  # find atmospheric pressure
    temperature = (float(mySensor.temperature_fahrenheit) / 1.16)  # find temperature
    date = str(datetime.datetime.now())
    time.sleep(sleepTime)  # force slowdown so pi doesn't get backed up and crash
    # print(humidity, atm_pressure, temperature)  # print for debugging purpose
    with open('/home/pi/atmBreakout.txt', '+a') as f:  # write text to file with append to store data
        f.write(date + "\n" + "Humidity: " + humidity + "\n")
        f.write(date + "\n" + "Pressure: " + atm_pressure + "\n")
        f.write(date + "\n" + "Temperature: " + str(temperature) + "\n")

    # print("true5" + atm_pressure)  # print for testing purposes
    # # Send via MQTT
    msg = [{'topic': "emon/ATMBreakout/Pressure", 'payload': float(atm_pressure)}]
    publish.multiple(msg, hostname=HostIP, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

    # print("true6" + temperature)  # print for testing purposes
    # Send via MQTT
    msg = [{'topic': "emon/ATMBreakout/Temperature", 'payload': float(temperature)}]
    publish.multiple(msg, hostname=HostIP, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

    # print("true7" + humidity)  # print for testing purposes
    # Send via MQTT
    msg = [{'topic': "emon/ATMBreakout/Humidity", 'payload': float(humidity)}]
    publish.multiple(msg, hostname=HostIP, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

if not mySensor.connected:
    print("The Qwiic BME280 device isn't connected to the system. Please check your connection",
          file=sys.stderr)
