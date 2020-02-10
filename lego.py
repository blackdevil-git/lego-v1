# coding=utf-8
import time
from time import sleep

from pylgbst import logging
from pylgbst.hub import MoveHub
from pylgbst.peripherals import EncodedMotor, TiltSensor, Current, Voltage, COLORS, COLOR_BLACK, COLOR_RED, COLOR_BLUE
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    hub = MoveHub()

    try:
        
        def callback(clr, distance):
            print("Color: %s / Distance: %s" % (clr, distance))
            if distance < 5:
                hub.led.set_color(COLOR_RED)
            elif distance > 5:
                hub.led.set_color(COLOR_BLUE)
            #    move(hub)
                

        hub.vision_sensor.subscribe(callback, mode=VisionSensor.COLOR_DISTANCE_FLOAT)

        hub.led.set_color(COLOR_BLUE)

        while True:
            sleep(1)
       
    finally:
        hub.vision_sensor.unsubscribe(callback)
        hub.disconnect()
        