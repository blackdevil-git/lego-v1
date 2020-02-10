# coding=utf-8
import time
from time import sleep

from pylgbst import logging
from pylgbst.hub import MoveHub
from pylgbst.peripherals import EncodedMotor, TiltSensor, Current, Voltage, COLORS, COLOR_BLACK
from pylgbst.hub import VisionSensor

log = logging.getLogger("demo")

data_distance = 0

def move(movehub):
    #log.info("Motors movement demo: angled")
    movehub.motor_external.start_speed(0.7)
    #movehub.motor_AB.start_speed(0.2, 0.2)

def stop(movehub):
    movehub.motor_external.stop()
    #movehub.motor_AB.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    hub = MoveHub()

    try:
        def callback(clr, distance):
            print("Color: %s / Distance: %s" % (clr, distance))
            #if distance < 5:
                #stop(hub)
            #else:
            #    move(hub)
                

        hub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_DISTANCE_FLOAT)

        move(hub)

        while True:
            sleep(1)
       
    finally:
        hub.vision_sensor.unsubscribe(callback)
        hub.disconnect()
        