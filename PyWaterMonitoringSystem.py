from __future__ import print_function
import paho.mqtt.publish as publish
import pyMultiSerial as p  # Create object of class pyMultiSerial
import serial
import qwiic_bme280
import sys
import datetime
import time
import requests

ms = p.MultiSerial()
ms.baudrate = 9600  # open serial port at 9600 to match Arduino's
ms.timeout = 2  # time it will take to retrieve data from the ports that are open
date = str(datetime.datetime.now())


# Callback function on detecting a port connection.
# Parameters: Port Number, Serial Port Object
# Return: True if the port is to be accepted, false if the port is to be rejected based on some condition within library
# For MQTT: publish multiple messages - this is a Python list of dict elements!
# topic parts: "emon" is required; "Sprinkler1" is a Node-name; "Moisture1" "GPM1", etc. are data labels

# Publish them via MQTT using the multiple method
# Do not need to specify a host since publishing internally

# Check if there are any ports open and if so continue
def port_connection_found_callback(portno, serial):
    print("Port Found: " + portno)


# register callback function
ms.port_connection_found_callback = port_connection_found_callback


# Callback on receiving port data
# Parameters: Port Number, Serial Port Object, Text read from port
def port_read_callback(portno, serial, text):

    # print(text)  # pull text from the port and print it for debugging purposes
    time.sleep(2)  # force slowdown so pi doesn't get backed up and crash

    # with open('GroundWater.txt', '+a') as f:  # write data to file GroundWater.txt stored on the pi
    #     f.write(date)  # write to text file
    #     f.write(text + "\n")

    # here im going to parse the text data coming in and turn it into ints then scale as necessary. Some data
    # is already scaled in the Arduino's such as percentages because it's not a lot of load for the arduino
    with open('portread.txt', '+w') as w:  # Open new file to store data only for each call back in order to read
        w.write(text + "\n")  # writing data to file without appending

    with open('portread.txt', 'r') as r:
        readline = r.readline()
        read_key = readline[0:4]  # read the first 4 characters of the file to get the pointer to the data
        print(read_key)

    # using the pointer set the correct data set to the data following the pointer
    if read_key == "gmcA":
        gmcA = str(readline[4: 10])  # read Data coming in
        print("true1 " + str(gmcA))  # print for testing purposes
        # Send via MQTT
        msg = [{'topic': "emon/Sprinkler1/Moisture1", 'payload': float(gmcA)}]
        publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

    if read_key == "gmcB":
        gmcB = str(readline[4: 10])  # read Data coming in
        print("true2 " + str(gmcB))  # print for testing purposes
        # Send via MQTT
        msg = [{'topic': "emon/Sprinkler1/Moisture2", 'payload': float(gmcB)}]
        publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

    if read_key == "preA":
        preA = str(readline[4: 10])  # read Data coming in
        print("true3 " + str(preA))  # print for testing purposes
        # Send via MQTT
        msg = [{'topic': "emon/Sprinkler1/Pressure1", 'payload': float(preA)}]
        publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

    else:  # if no data found then return out and look for more
        print("No data was found. looking for more")

    breakout_sensor()  # calls for function breakout sensor
    with open('atmBreakoutRead.txt', 'r') as a:
        for x in a:
            read_line_break = x
            # read first 4 characters of the file to get the pointer to the data
            read_key_break = read_line_break[0: 4]
            print(read_key_break)

            if read_key_break == "preO":
                preO = str(readline[4: 20])  # read Data coming in
                print("true5" + str(preO))  # print for testing purposes
                # Send via MQTT
                msg = [{'topic': "emon/ATMBreakout/Pressure", 'payload': float(preO)}]
                publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

            if read_key_break == "temp":
                temp = str(readline[4: 20])  # read Data coming in
                print("true6" + str(temp))  # print for testing purposes
                # Send via MQTT
                msg = [{'topic': "emon/ATMBreakout/Temperature", 'payload': float(temp)}]
                publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

            if read_key_break == "humd":
                humd = str(readline[4: 20])  # read Data coming in
                print("true7" + str(humd))  # print for testing purposes
                # Send via MQTT
                msg = [{'topic': "emon/ATMBreakout/Humidity", 'payload': float(humd)}]
                publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

            else:  # if no data found then return out and look for more
                print("No data was found. looking for more")


# register callback function
ms.port_read_callback = port_read_callback


# Callback on port disconnection. Triggered when a device is disconnected from port.
# Parameters: Port No
def port_disconnection_callback(portno):
    print("Port " + portno + " disconnected")


# register callback function
ms.port_disconnection_callback = port_disconnection_callback


def breakout_sensor():
    global humidity, atm_pressure, temperature

    mySensor = qwiic_bme280.QwiicBme280()
    mySensor.begin()  # start atm breakout sensor

    if mySensor.connected:
        hum_scaled = (int(mySensor.humidity) + 10.0)
        humidity = (str(hum_scaled))  # find humidity
        atm_pressure = (str(mySensor.pressure))  # find atmospheric pressure
        temperature = (str(mySensor.temperature_fahrenheit))  # find temperature
        time.sleep(2)  # force slowdown so pi doesn't get backed up and crash
        # print(humidity, atm_pressure, temperature)  # print for debugging purpose
        with open('atmBreakout.txt', '+a') as f:  # write text to file with append to store data
            f.write(date + "\n" + "Humidity: " + humidity + "\n")
            f.write(date + "\n" + "Pressure: " + atm_pressure + "\n")
            f.write(date + "\n" + "Temperature: " + temperature + "\n")
        with open('atmBreakoutRead.txt', '+w') as i:     # write to file while writing over old text for MQTT send
            i.write("humd" + humidity + "\n")
            i.write("preO" + atm_pressure + "\n")
            i.write("temp" + temperature + "\n")
        return

    if not mySensor.connected:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection",
              file=sys.stderr)
        return


# Start Monitoring ports
ms.Start()

# Any code written below ms.Start() will be executed only after monitoring is stopped.
