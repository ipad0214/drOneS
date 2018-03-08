import threading
import message_model
import os

if os.uname()[4][:3] == 'arm':
    import RPi.GPIO as board

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
                queue_resp = hardware_queue.get(block=False)

                if queue_resp is message_model.GpioModel:
                    self.set_websocket_status_led(queue_resp.websocket_led)
                    self.set_websocket_sending_led(queue_resp.websocket_receive_led)
                    self.set_websocket_receiving_led(queue_resp.websocket_sending_led)


    @staticmethod
    def set_websocket_status_led(value):
        set_led(websocket_status_pin, value)

    @staticmethod
    def set_websocket_receiving_led(value):
        set_led(websocket_receiving_pin, value)

    @staticmethod
    def set_websocket_sending_led(value):
        set_led(websocket_sending_pin, value)


def run(hardware_queue, message_queue):
    controller = HardwareController(hardware_queue=hardware_queue, message_queue=message_queue)
