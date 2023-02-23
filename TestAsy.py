from __future__ import print_function
import asyncio
import serial_asyncio
import serial
from serial_device2 import SerialDevice, find_serial_device_ports

ser = serial.Serial()
ser.braudrate = 9600


print(find_serial_device_ports())  # Returns list of available serial ports
portList = find_serial_device_ports()
comA = portList[0]
comB = portList[1]


class InputChunkProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print(data)

        # stop callbacks again immediately
        self.pause_reading()

    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        self.transport.resume_reading()


async def reader():
    transportA, protocolA = await serial_asyncio.create_serial_connection(loop, InputChunkProtocol, comA,
                                                                          ser.baudrate)
    transportB, protocolB = await serial_asyncio.create_serial_connection(loop, InputChunkProtocol, comB,
                                                                          ser.baudrate)
    while True:
        await asyncio.sleep(0.3)
        protocolA.resume_reading()
        protocolB.resume_reading()


loop = asyncio.get_event_loop()
loop.run_until_complete(reader())
loop.close()
