from __future__ import print_function
import asyncio
import serial_asyncio
import serial
from serial_device2 import SerialDevice, find_serial_device_ports
import paho.mqtt.publish as publish
import datetime
import time

ser = serial.Serial()
ser.braudrate = 9600

# print(find_serial_device_ports())  # Returns list of available serial ports
portList = find_serial_device_ports()
comA = portList[0]
comB = portList[1]


class InputChunkProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    # Takes data in from the ports and writes to file and sends to emoncms
    def data_received(self, data):
        data_decoded = data.decode()  # data comes in, in bytes so parse to strings
        # print(data_decoded)
        with open('GroundWater.txt', '+a') as f:  # write data to file GroundWater.txt stored on the pi
            date = str(datetime.datetime.now())
            f.write(date)  # write to text file
            f.write(str(data_decoded) + '\n')

        x = data_decoded.partition(":")  # separate two numbers by a : and store them in tuple
        # print(x)  # print tuple to check

        read_key = str(x[0])  # first entry into tuple is the first set of data
        read_keyB = str(x[2])   # second entry into tuple is the second set of data

        # Since data is always coming in, in the same way we know the first entry is the first sensor and second is
        # second sensor
        if read_key[0:3] == "gmc":
            gmcA = str(read_key[4:10])  # read Data coming in
            # print("true1 " + str(gmcA))  # print for testing purposes
            # Send via MQTTa
            msg = [{'topic': "emon/Sprinkler1/Moisture1", 'payload': float(gmcA)}]
            publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

            gmcB = str(read_keyB[4: 10])  # read Data coming in
            # print("true2 " + str(gmcB))  # print for testing purposes
            # Send via MQTT
            msg = [{'topic': "emon/Sprinkler1/Moisture2", 'payload': float(gmcB)}]
            publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})
            time.sleep(2)

        # Since data is always coming in, in the same way we know the first entry is the first sensor and second is
        # second sensor
        elif read_key[0:3] == "pre":
            preA = str(read_key[4: 10])  # read Data coming in
            # print("true3 " + str(preA))  # print for testing purposes
            # Send via MQTT
            msg = [{'topic': "emon/Sprinkler1/Pressure1", 'payload': float(preA)}]
            publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})

            preB = float(read_keyB[4: 10])  # read Data coming in
            # print("true4 " + str(preB))  # print for testing purposes
            # Send via MQTT
            msg = [{'topic': "emon/Sprinkler1/Pressure2", 'payload': float(preB)}]
            publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})
            time.sleep(2)

        # stop callbacks again immediately
        self.pause_reading()

    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        self.transport.resume_reading()


async def reader():
    # sets port open for first port in list
    transportA, protocolA = await serial_asyncio.create_serial_connection(loop, InputChunkProtocol, comA,
                                                                          ser.baudrate)
    # sets port open for second port in list
    transportB, protocolB = await serial_asyncio.create_serial_connection(loop, InputChunkProtocol, comB,
                                                                          ser.baudrate)
    while True:
        await asyncio.sleep(0.3)  # time until new data is grabbed (can be changed to preference)
        protocolA.resume_reading()
        protocolB.resume_reading()


loop = asyncio.get_event_loop()
loop.run_until_complete(reader())
loop.close()
