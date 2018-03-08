import threading
import message_model
import os

if os.uname()[4][:3] == 'arm':
    import RPi.GPIO as board
else:
    print("ERROR: NOT RUNNING ON PI => NO GPIO OUTPUT")

websocket_status_pin = 11
websocket_receiving_pin = 10
websocket_sending_pin = 9
nrf_status_pin = 12


def setup_gpio():
    board.setwarnings(False)
    board.setmode(board.BOARD)
    board.setup(nrf_status_pin, board.OUT)
    board.setup(websocket_status_pin, board.OUT)
    board.setup(websocket_receiving_pin, board.OUT)
    board.setup(websocket_sending_pin, board.OUT)


def set_led(pin, status):
        board.output(pin, status if board.HIGH else board.LOW)


class HardwareController:
    def __init__(self, hardware_queue, message_queue):
        self.hardware_model = message_model._HardwareModel()

        setup_gpio()

        while True:
            if not hardware_queue.empty():
                self.hardware_model.LED = hardware_queue.get(block=False).LED

                self.set_websocket_status_led(self.hardware_model.Websocket_LED)

    @staticmethod
    def set_websocket_status_led(value):
        set_led(websocket_status_pin, value)


def run(hardware_queue, message_queue):
    controller = HardwareController(hardware_queue=hardware_queue, message_queue=message_queue)
