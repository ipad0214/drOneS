import serial
import message_model
from time import sleep
import RPi.GPIO as GPIO

class ArduinoBridgeThread:
    def __init__(self, q, arduino_queue, hardware_queue):
        self.arduino_queue = arduino_queue
        self.q = q
        self.hardware_model = message_model._HardwareModel()
        self.serial_port = serial.Serial('/dev/ttyUSB0', baudrate=115200)
        self.serial_port.timeout = 0
        sleep(2)
        self.create_gpio_output()
        print("serial ready for fire")

        while True:
            if not arduino_queue.empty():
                #self.hardware_model.LED = hardware_queue.get(block=False).LED
                led_status = arduino_queue.get(block=False).LED
                self.send_to_arduino(led_status)

    def create_gpio_output(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)

    def send_to_arduino(self, status):
        if status:
            self.serial_port.write(b"SE001001")
            GPIO.output(11, GPIO.HIGH)
            sleep(1./120)
        else:
            self.serial_port.write(b"SE001000")
            GPIO.output(11, GPIO.LOW)
            sleep(1. / 120)

