import logging
import time
import requests
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
import time
import vlc

# from grove.grove_mini_pir_motion_sensor import GroveMiniPIRMotionSensor
# from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
# from Seeed_Python_DHT.seeed_dht import DHT
# from grove.grove_moisture_sensor import GroveMoistureSensor
# from grove.button import Button
# from grove.grove_ryb_led_button import GroveLedButton
# from grove.grove_light_sensor_v1_2 import GroveLightSensor
# from grove.grove_servo import GroveServo
# import seeed_dht
import random
# from grover import *
# from relay import *
# from tds import EC

# Configuration of logger, in this case it will send messages to console
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

log = logging.getLogger(__name__)

thingsboard_server = 'stg-smartagri.maxisiotplatform.com'
access_token = 'mGWcxj0Cy9X6gJJlITDy'

light_state = False
water_state = False
fert_state = False

def main():

    # Callback for server RPC requests (Used for control servo and led blink)
    def on_server_side_rpc_request(request_id, request_body):
        light_state = False
        water_state = False
        fert_state = False
        log.info('received rpc: {}, {}'.format(request_id, request_body))
        if request_body['method'] == 'getLightState':
            client.send_rpc_reply(request_id, light_state)
            # print(request_body['getLightState']['params'])
        elif request_body['method'] == 'getFertState':
            client.send_rpc_reply(request_id, fert_state)
            print(request_body['getFertState']);
        elif request_body['method'] == 'getWaterState':
            client.send_rpc_reply(request_id, water_state)

    # Connecting to ThingsBoard
    client = TBDeviceMqttClient(thingsboard_server, 1883 ,access_token)
    client.set_server_side_rpc_request_handler(on_server_side_rpc_request)
    client.connect()
    start = time.time()

    while True:
        end = time.time()
        if end-start > 10:

            # distance = ultrasonic_sensor.get_distance()
            # ultrasonicA = volume(grover.get_distance())
            # ultrasonicB = volume(grover2.get_distance())
            # ultrasonicC = volume(grover3.get_distance())
            # tdsValue = EC.TDS()
            # ultrasonicA = random.randint(300,310)
            # ultrasonicB = random.randint(300,310)
            # ultrasonicC = random.randint(500,510)
            # tdsValue = random.randint(400,430)
            # temp = temper()
            # log.debug('ultrasonicA: {} cm'.format(ultrasonicA))
            # log.debug('ultrasonicB: {} cm'.format(ultrasonicB))
            # log.debug('ultrasonicC: {} cm'.format(ultrasonicC))

            # log.debug('temperature: {}C, humidity: {}%'.format(temp[1], temp[0]))

            # log.debug('tds: {}'.format(tdsValue))

            # log.debug('light: {}'.format(light_sensor.light))

            # Formatting the data for sending to ThingsBoard
            # telemetry = {'UltrasonicA': ultrasonicA,
            #              'UltrasonicB': ultrasonicB,
            #              'UltrasonicC': ultrasonicC,
            #              'TDSValue': tdsValue,
            #              'Temp': temp[1],
            #              'Hum': temp[0],
            #              'deviceId':'testPC'}
            #             #  'light': light_sensor.light}

            # # Sending the data
            # client.send_telemetry(telemetry).get()

            start = time.time()
            print("Message Sent")



if __name__ == '__main__':
    main()
