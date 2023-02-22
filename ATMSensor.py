from __future__ import print_function
import paho.mqtt.publish as publish
import qwiic_bme280
import sys
import datetime
import time


def breakout():
    breakout_sensor()
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


def breakout_sensor():
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
        with open('atmBreakoutRead.txt', '+w') as i:  # write to file while writing over old text for MQTT send
            i.write("humd" + humidity + "\n")
            i.write("preO" + atm_pressure + "\n")
            i.write("temp" + temperature + "\n")
        return

    if not mySensor.connected:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection",
              file=sys.stderr)
        return
