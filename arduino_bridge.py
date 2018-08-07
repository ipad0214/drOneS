import serial
import message_model
from time import sleep
import os

if os.uname()[4][:3] == 'arm':
    import RPi.GPIO as GPIO


class ArduinoBridgeThread:
    def __init__(self, q, arduino_queue, hardware_queue=None):
        if os.uname()[4][:3] == 'arm':
            self.arduino_queue = arduino_queue
            self.q = q
            self.serial_port = serial.Serial('/dev/ttyUSB0', baudrate=115200)
            self.serial_port.timeout = 0

        while True:
            if not arduino_queue.empty():
                if arduino_queue is not None:
                    queue_resp = arduino_queue.get(block=False)
                    
                    
def run(hardware_queue, message_queue, arduino_queue):
    controller = ArduinoBridgeThread(q=message_queue, arduino_queue=arduino_queue, hardware_queue=hardware_queue)