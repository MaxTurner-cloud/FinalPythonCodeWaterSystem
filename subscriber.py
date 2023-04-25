# subscriber.py
import paho.mqtt.client as mqtt

hostOne = "172.31.171.113"


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect if reconnect after losing the connection with the broker,
    # it will continue to subscribe to
    client.subscribe("emon/Sprinkler1/Moisture1")


# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send
# the will message to other clients
client.will_set('raspberry/status', b'{"status": "Off"}')

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect(hostOne, 1883, 60, 'emonpi', 'emonpimqtt2016')

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
