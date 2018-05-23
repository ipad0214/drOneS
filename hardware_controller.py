import message_model
import os
import time

if os.uname()[4][:3] == 'arm':
    import RPi.GPIO as board

websocket_status_pin = 11
websocket_receiving_pin = 10
websocket_sending_pin = 9
nrf_status_pin = 12


def setup_gpio(isOnPi):
    if isOnPi:
        board.setwarnings(False)
        board.setmode(board.BOARD)
        board.setup(nrf_status_pin, board.OUT)
        board.setup(websocket_status_pin, board.OUT)
        board.setup(websocket_receiving_pin, board.OUT)
        board.setup(websocket_sending_pin, board.OUT)


def set_led(pin, permanent=False):
    if not os.uname()[4][:3] == "arm":
        print("pin: {}, status: ON".format(pin))
        if permanent:
            return
        time.sleep(.50)
        print("pin: {}, status: OFF".format(pin))
        return

    board.output(pin, board.HIGH)
    print("pin: {}, status: ON".format(pin))
    if permanent:
        return
    time.sleep(.50)
    board.output(pin, board.LOW)
    print("pin: {}, status: OFF".format(pin))


def set_led_off(pin):
    board.output(pin, board.LOW)


class HardwareController:
    def __init__(self, hardware_queue, message_queue):
        self.hardware_model = message_model.GpioModel()
        self.isOnPi = os.uname()[4][:3] == "arm"

        setup_gpio(self.isOnPi)

        while True:
            if not hardware_queue.empty():
                queue_resp = hardware_queue.get(block=False)

                if type(queue_resp) is message_model.GpioModel:
                    self.set_websocket_status_led(queue_resp)
                    self.set_websocket_sending_led(queue_resp)
                    self.set_websocket_receiving_led(queue_resp)

    @staticmethod
    def set_websocket_status_led(queue_resp):
        if queue_resp.websocket_led:
            set_led(websocket_status_pin, permanent=True)
        else:
            set_led_off(websocket_status_pin)

    @staticmethod
    def set_websocket_sending_led(queue_resp):
        if queue_resp.websocket_sending_led:
            set_led(websocket_sending_pin)

    @staticmethod
    def set_websocket_receiving_led(queue_resp):
        if queue_resp.websocket_receiving_led:
            set_led(websocket_receiving_pin)


def run(hardware_queue, message_queue):
    controller = HardwareController(hardware_queue=hardware_queue, message_queue=message_queue)

