#!/usr/bin/python

import time, sys, requests
from grove.adc import ADC

class CustomAlcoholSensor(object):
    # Pass the channel that the sensor is connected to.
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
    
    @property
    def value(self):
        RS_air = 33.0
        ratio = 0.0
        sensorValue = 0.0
        for i in range(1500):
            sensorValue = sensorValue + float(self.adc.read(self.channel))
            time.sleep(0.001)
        sensorValue = sensorValue / 1500.0
        sensorVolt = sensorValue/1024*5.0
        RS_gas = float(sensorVolt/(5.0 - sensorVolt))
        print("RS_gas: {}".format(RS_gas))
        ratio = RS_gas/RS_air

        return ratio

def main():
    sensor  = CustomAlcoholSensor(2)
    
    url = "https://iot-visual.vercel.app/api/postData?_vercel_no_cache=1"

    print("Reading")
    value = sensor.value
    time.sleep(1)
    print(value)
    if (value <= 0.01):
    # Send POST req to server
        body = {
        "rpi": "lab1",
        "owner": "amazon",
        "arranca": False
        }
        # Now do the post req
        requests.post(url, json = body)
    else:
        body = {
        "rpi": "lab1",
        "owner": "amazon",
        "arranca": True
        }
        # Do the req
        requests.post(url, json = body)
        time.sleep(1)

if __name__ == '__main__':
    main()
