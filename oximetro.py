from lib.MAX30102 import MAX30102
from utime import sleep
import lib.logging as logging

logging.basicConfig(level=logging.INFO)

sensor = MAX30102()

sensor.setup_sensor()
sensor.setSampleRate(400)
sensor.setFIFOAverage(32)
sensor.setADCRange(4096)
sensor.setPulseWidth(118)
sensor.setLEDMode(2)


print(sensor.readTemperature())

while True:
    sensor.check()
    if(sensor.available()):
        red_sample  = sensor.popRedFromStorage()
        IR_reading = sensor.popIRFromStorage()
        acquisition_rate = sensor.getAcquisitionFrequency()
        temperature_C = sensor.readTemperature()
        hr=sensor.getReadPointer();
        
        
        print(red_sample, ",", IR_reading, ", ", acquisition_rate, ", ",temperature_C)
        

    sleep(2)