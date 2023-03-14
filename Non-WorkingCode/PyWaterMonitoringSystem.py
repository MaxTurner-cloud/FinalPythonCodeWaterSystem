from __future__ import print_function
import paho.mqtt.publish as publish
import pyMultiSerial as p  # Create object of class pyMultiSerial
import serial
import qwiic_bme280
import sys
import datetime
import time

ms = p.MultiSerial()
ms.baudrate = 9600  # open serial port at 9600 to match Arduino's
ms.timeout = 1  # time it will take to retrieve data from the ports that are open
date = str(datetime.datetime.now())


# Callback function on detecting a port connection. Parameters: Port Number, Serial Port Object Return: True if the
# port is to be accepted, false if the port is to be rejected based on some condition within library For MQTT:
# publish multiple messages - this is a Python list of dict elements! topic parts: "emon" is required; "Sprinkler1"
# is a Node-name; "Moisture1, Pressure1, ... etc" "GPM1", etc. are data labels

# Check if there are any ports open and if so continue
def port_connection_found_callback(portno, serial):
    print("Port Found: " + portno)


# register callback function
ms.port_connection_found_callback = port_connection_found_callback


# Callback on receiving port data
# Parameters: Port Number, Serial Port Object, Text read from port
def port_read_callback(portno, serial, text):

    # print(text)  # pull text from the port and print it for debugging purposes

    with open('GroundWater.txt', '+a') as f:  # write data to file GroundWater.txt stored on the pi
        f.write(date)  # write to text file
        f.write(text + "\n")

    # here im going to parse the text data coming in and turn it into ints then scale as necessary. Some data
    # is already scaled in the Arduino's such as percentages because it's not a lot of load for the arduino

    read_key = text[0:4]  # read the first 4 characters of the file to get the pointer to the data
    print(read_key)

    # using the pointer set the correct data set to the data following the pointer
    if read_key == "gmcA":
        gmcA = str(text[4: 10])  # read Data coming in
        print("true1 " + str(gmcA))  # print for testing purposes
        # Send via MQTT
        msg = [{'topic': "emon/Sprinkler1/Moisture1", 'payload': float(gmcA)}]
        publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})
        time.sleep(5)
        return

    elif read_key == "gmcB":
        gmcB = str(text[4: 10])  # read Data coming in
        print("true2 " + str(gmcB))  # print for testing purposes
        # Send via MQTT
        msg = [{'topic': "emon/Sprinkler1/Moisture2", 'payload': float(gmcB)}]
        publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})
        time.sleep(5)
        return

    elif read_key == "preA":
        preA = str(text[4: 10])  # read Data coming in
        print("true3 " + str(preA))  # print for testing purposes
        # Send via MQTT
        msg = [{'topic': "emon/Sprinkler1/Pressure1", 'payload': float(preA)}]
        publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})
        time.sleep(5)
        return

    elif read_key == "preB":
        preB = float(text[4: 10])    # read Data coming in
        print("true4 " + str(preB))  # print for testing purposes
        # Send via MQTT
        msg = [{'topic': "emon/Sprinkler1/Pressure2", 'payload': float(preB)}]
        publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})
        time.sleep(5)
        return

    else:  # if no data found then return out and look for more
        print("No data was found. looking for more")
        return


# register callback function
ms.port_read_callback = port_read_callback


# Callback on port disconnection. Triggered when a device is disconnected from port.
# Parameters: Port No
def port_disconnection_callback(portno):
    print("Port " + portno + " disconnected")


# register callback function
ms.port_disconnection_callback = port_disconnection_callback

# Start Monitoring ports
ms.Start()

# Any code written below ms.Start() will be executed only after monitoring is stopped.
