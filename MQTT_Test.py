from __future__ import print_function
import paho.mqtt.publish as publish

GPM1 = 1
Temperature1 = 10
Rotation1_RPM = 20
gmcA = 15
gmcB = 12
preA = 300
preB = 250

# publish multiple messages - this is a Python list of dict elements!
# topic parts: "emon" is required; "Sprinkler1" is a Node-name; "Moisture1" "GPM1", etc. are data labels
msg = [{'topic': "emon/Sprinkler1/Moisture1", 'payload': gmcA},
       {'topic': "emon/Sprinkler1/Moisture2", 'payload': gmcB},
       {'topic': "emon/Sprinkler1/Pressure1", 'payload': preA},
       {'topic': "emon/Sprinkler1/Pressure2", 'payload': preB},
       {'topic': "emon/Sprinkler1/GPM1", 'payload': GPM1},
       {'topic': "emon/Sprinkler1/Temperature1", 'payload': Temperature1},
       {'topic': "emon/Sprinkler1/Rotation1_RPM", 'payload': Rotation1_RPM}]

# Publish them via MQTT using the multiple method
# Do not need to specify a host since publishing internally
publish.multiple(msg, auth={'username': "emonpi", 'password': "emonpimqtt2016"})
