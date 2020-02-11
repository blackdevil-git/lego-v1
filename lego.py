#!/usr/bin/env python3
import time
from time import sleep

from pylgbst import logging
from pylgbst.hub import MoveHub
from pylgbst import get_connection_auto
from pylgbst.peripherals import EncodedMotor, TiltSensor, Current, Voltage, COLORS, COLOR_BLACK, COLOR_RED, COLOR_BLUE, COLOR_YELLOW
from pylgbst.hub import VisionSensor

log = logging.getLogger("autobot")

data_distance = None

motor_state = None

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
                #hub.led.set_color(COLOR_RED)
                #stop(hub)
                sleep(1)
            elif distance <= 5:
                #hub.led.set_color(COLOR_YELLOW)
                #moveslow(hub)
                sleep(1)
            elif distance > 5:
                #hub.led.set_color(COLOR_BLUE)
                #movefast(hub)
                sleep(1)
            else:
                #stop(hub)
                #hub.led.set_color(COLOR_BLACK)
                sleep(1)

def connect():
    #hub.connection.connect()
    sleep(1)

def button_callback(is_pressed):
    global motor_state
    print("Btn pressed: %s" % is_pressed)
    if is_pressed == 2:
        if motor_state == 0:
            motor_state = 1
        else:
            motor_state = 0

def main():
    
    logging.basicConfig(level=logging.INFO)

    global motor_state
   

    try:
        motor_state = 0
        hub = MoveHub()

        hub.button.subscribe(button_callback)

        #hub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_DISTANCE_FLOAT)

        while True:

            if motor_state ==  0:
                stop(hub)
            else:
                moveslow(hub)

            if hub.connection.is_alive():
                print("hub 2 connected!")
            else:
                print("hub 2 disconnected!")

            #if not hub.connection.is_alive():
            #    connect()
            #    hub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_DISTANCE_FLOAT)
            #    print("Reconnection!")
            #else:
            #    print("Connected!")
            sleep(5)
       
    finally:
        #hub.vision_sensor.unsubscribe(callback)
        #hub.disconnect()
        hub.disconnect()

if __name__ == '__main__':
    main()
    
        