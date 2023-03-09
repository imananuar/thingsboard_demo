import time
import seeed_dht
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

thingsboard_server = 'stg-smartagri.maxisiotplatform.com'
access_token = "iBbdZyImStaWIZRWpzMB"


def temper():
    sensor = seeed_dht.DHT("11", 18)
    humi, temp = sensor.read()
    return humi, temp


def main():

    # Connect to Thingsboard
    client = TBDeviceMqttClient(thingsboard_server, 1883 ,access_token)
    client.connect()
    start = time.time()

    while True:
        end = time.time()
        if end-start > 10:
            # Read and display the temperature data
            temp = temper()
            message = 'Temperature: {}C, Humidity: {}%'.format(temp[1], temp[0]

            #Format the data in Json to send to thingsboard
            telemetry = {"temperature": temp[1], "humidity": temp[0]}

            #Send the data
            client.send_telemetry(telemetry).get()
            start = time.time()
            print("Message sent! " + message)
        


if __name__ == '__main__':
    main()