import os
import json
import threading
import requests
import time
import seeed_dht
from six.moves import input
from azure.iot.device import IoTHubDeviceClient, MethodResponse, Message

from grover import *
from relay import *
from tds import EC
#from light import cahaya
#from temp import temhum

conn_str = "HostName=mbec-prd-iot-hub.azure-devices.net;DeviceId=hydroponic-01;SharedAccessKey=FmIz6fUlqBVP/TCFt28w2xJzFR2ThyqR2spQIWyniVI="


device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

start = 0
device_client.connect()

def onLight():
    x = requests.get('http://192.168.1.107/cm?cmnd=Power%20On')
    
def offLight():
    x = requests.get('http://192.168.1.107/cm?cmnd=Power%20Off')

def temper():
    sensor = seeed_dht.DHT("11",12)
    humi, temp = sensor.read()
    return humi, temp

def releaseFert(awake):
    Grove1.on()
    Grove2.on()
    time.sleep(awake)
    Grove1.off()
    Grove2.off()

def releaseWater(awake):
    Grove3.on()
    time.sleep(awake)
    Grove3.off()

def releaseFertOn():
    Grove1.on()
    Grove2.on()

def releaseFertOff():
    Grove1.off()
    Grove2.off()
    time.sleep(4)

def releaseWaterOn():
    Grove3.on()

def releaseWaterOff():
    Grove3.off()

def send():
    time.sleep(2)
    ultrasonicA = volume(grover.get_distance())
    ultrasonicB = volume(grover2.get_distance())
    ultrasonicC = volume(grover3.get_distance())
    tdsValue = EC.TDS()
    #uv = cahaya.light()
    temp = temper()
    
    payload = json.dumps(
        {
            'UltrasonicA':ultrasonicA,
            'UltrasonicB':ultrasonicB,
            'UltrasonicC':ultrasonicC,
            'TDSValue':tdsValue,
            #'Light':uv,
            'Temp':temp[1],
            'Hum':temp[0],
            'deviceId':'hydroponic-01'
            #'Temp':23,
            #'Hum':64
            })
    msg = Message(payload)
    print(payload)
    device_client.send_message(msg)

def method_request_handler(method_request):
    if method_request.name == "lightOff":
        payload = {"result":True,"data":"Light Toggle"}
        status = 200
        print("executed")
        offLight()
        send()
    elif method_request.name == "lightOn":
        payload = {"result":True,"data":"Light Toggle"}
        status = 200
        print("executed")
        OnLight()
        send()
    elif method_request.name == "waterOn":
        payload = {"result":True,"data":"Light Toggle"}
        status = 200
        print("executed")
        releaseWater(5)
        send()
    elif method_request.name == "waterOff":
        payload = {"result":True,"data":"Light Toggle"}
        status = 200
        print("executed")
        releaseWater(5)
        send()
    elif method_request.name == "fertOn":
        payload = {"result":True,"data":"Light Toggle"}
        status = 200
        print("executed")
        releaseFert(5)
        send()
    elif method_request.name == "fertOff":
        payload = {"result":True,"data":"Light Toggle"}
        status = 200
        print("executed")
        releaseFert(5)
        send()
    else:
        payload = {"result":False,"data":"Unknown"}
        status=400
        
    method_response = MethodResponse.create_from_method_request(method_request,status,payload)
    device_client.send_method_response(method_response)
    
def message_handler(message):
    print("the data in the message received was ")
    print(message.data)
    method_D = message.data.decode('utf-8')
    if "lightOn" in method_D:
        print("Light ON")
        onLight()
        send()
    elif "lightOff" in method_D:
        print("Light OFF")
        offLight()
        send()
    elif "waterOn" in method_D:
        print("Water ON")
        releaseWaterOn()
    elif "waterOff" in method_D:
        print("Water OFF")
        releaseWaterOff()
        send()
    elif "fertOn" in method_D:
        print("Fert ON")
        releaseFertOn()
    elif "fertOff" in method_D:
        print("Fert OFF")
        releaseFertOff()
        send()
    elif "fertAuto" in method_D:
        print("Fert Auto")
        releaseFert(5)
    elif "waterAuto" in method_D:
        print("Water Auto")
        releaseWater(5)
        
device_client.on_message_received = message_handler
device_client.on_method_request_received = method_request_handler

while True:
    #tdsValue = EC.TDS()
    #print(tdsValue)
    end = time.time()
    #if tdsValue < 500 and end-start > 300:
       # releaseFert(5)
       # send()
       # print("Fert released due to low TDS")
       # start = time.time()
    if end-start > 1080:
        start = time.time()
        send()
        print("Message Sent")
