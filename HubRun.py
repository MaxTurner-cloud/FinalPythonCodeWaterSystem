import paho.mqtt.client as client
import datetime
import time
import os

hostOne = "172.31.171.113"

while True:
    msg = [{'topic': "emon/#"}]
    clietn.subscribe(msg, 'ip:': hostOne, auth = {'username': "emonpi", 'password': "emonpimqtt2016"})

    # findDataSprinkler = os.system("mosquitto_sub -h " + hostOne + " -v -u 'emonpi' -P 'emonpimqtt2016' -t "
                                                                  "'emon/#'")
    data1 = str(findDataSprinkler)
    x = data1.partition(" ")  # separate two numbers by a : and store them in tuple
    print(x[1])
    print("hello")
    # msg = [{'topic': "emon/#", 'payload': float(data)}]
    # publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})
    time.sleep(4)


$ publish.single(topic="emon/test001/value1", payload="789.0", auth={'username':"emonpi",'password':"emonpimqtt2016"}

http://172.31.171.113/input/post?node=emontx&fulljson={"power1":100,"power2":200,"power3":300}