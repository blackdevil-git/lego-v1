#!/usr/bin/env python3
import time
from time import sleep

from pylgbst import logging
from pylgbst.hub import MoveHub
from pylgbst.hub import Hub
from pylgbst import get_connection_auto
from pylgbst.peripherals import EncodedMotor, TiltSensor, Current, Voltage, COLORS, COLOR_BLACK, COLOR_RED, COLOR_BLUE, COLOR_YELLOW
from pylgbst.hub import VisionSensor

mhub = MoveHub()

log = logging.getLogger("autobot")

data_distance = 0

def movefast(movehub):
    #log.info("Motors movement demo: angled")
    movehub.motor_external.start_speed(0.3)
    movehub.motor_AB.start_speed(0.3, 0.2)

def moveslow(movehub):
    #log.info("Motors movement demo: angled")
    movehub.motor_external.start_speed(0.1)
    movehub.motor_AB.start_speed(0.1, 0.1)

def stop(movehub):
    movehub.motor_external.stop()
    #movehub.motor_AB.stop()

def demo_led_colors(movehub):
    # LED colors demo
    log.info("LED colors demo")

    # We get a response with payload and port, not x and y here...
    def colour_callback(**named):
        log.info("LED Color callback: %s", named)

    movehub.led.subscribe(colour_callback)
    for color in list(COLORS.keys())[1:] + [COLOR_BLACK]:
        log.info("Setting LED color to: %s", COLORS[color])
        movehub.led.set_color(color)
        sleep(1)


def callback(clr, distance):
            print("Color: %s / Distance: %s" % (clr, distance))
            if distance <= 2:
                mhub.led.set_color(COLOR_RED)
                stop(mhub)
            elif distance <= 5:
                mhub.led.set_color(COLOR_YELLOW)
                moveslow(mhub)
            elif distance > 5:
                mhub.led.set_color(COLOR_BLUE)
                movefast(mhub)
            else:
                stop(mhub)
                mhub.led.set_color(COLOR_BLACK)

def connect():
    mhub.connection.connect()


def main():
    logging.basicConfig(level=logging.INFO)
    conn = get_connection_auto()  # ! don't put this into `try` block

    try:
        try:
            hub = Hub(conn)
        finally:
            conn.disconnect()
                
        mhub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_DISTANCE_FLOAT)

        while True:
            if not hub.connection.is_alive:
                connect()
                mhub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_DISTANCE_FLOAT)
                print("Reconnection!")
            else:
                print("Connected!")
            sleep(5)
       
    finally:
        mhub.vision_sensor.unsubscribe(callback)
        hub.disconnect()

if __name__ == '__main__':
    main()
    
        