# coding=utf-8
import time
from time import sleep

from pylgbst import *
from pylgbst.hub import MoveHub
from pylgbst.peripherals import EncodedMotor, TiltSensor, Current, Voltage, COLORS, COLOR_BLACK
from pylgbst.hub import VisionSensor

log = logging.getLogger("demo")

data_distance = 0

DEMO_CHOICES = {
    
}

def get_options():
    import argparse
    arg_parser = argparse.ArgumentParser(
        description='Demonstrate move-hub communications',
    )
    arg_parser.add_argument(
        '-c', '--connection',
        default='auto://',
        help='''Specify connection URL to use, `protocol://mac?param=X` with protocol in:
    "gatt","pygatt","gattlib","gattool", "bluepy","bluegiga"'''
    )
    arg_parser.add_argument(
        '-d', '--demo',
        default='all',
        choices=sorted(DEMO_CHOICES.keys()),
        help="Run a particular demo, default all"
    )
    return arg_parser

def connection_from_url(url):
    import pylgbst
    if url == 'auto://':
        return None
    try:
        from urllib.parse import urlparse, parse_qs
    except ImportError:
        from urlparse import urlparse, parse_qs
    parsed = urlparse(url)
    name = 'get_connection_%s' % parsed.scheme
    factory = getattr(pylgbst, name, None)
    if not factory:
        msg = "Unrecognised URL scheme/protocol, expect a get_connection_<protocol> in pylgbst: %s"
        raise ValueError(msg % parsed.protocol)
    params = {}
    if parsed.netloc.strip():
        params['hub_mac'] = parsed.netloc
    for key, value in parse_qs(parsed.query).items():
        if len(value) == 1:
            params[key] = value[0]
        else:
            params[key] = value
    return factory(
        **params
    )


def move(movehub):
    #log.info("Motors movement demo: angled")
    movehub.motor_external.start_speed(0.2)
    #movehub.motor_AB.start_speed(0.2, 0.2)

def stop(movehub):
    movehub.motor_external.stop()
    #movehub.motor_AB.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = get_options()
    options = parser.parse_args()
    parameters = {}
    try:
        connection = connection_from_url(options.connection)
        parameters['connection'] = connection
    except ValueError as err:
        parser.error(err.args[0])

    hub = MoveHub(**parameters)

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
        