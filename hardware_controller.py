import threading
import RPi.GPIO as board
import message_model

def setup_GPIO():
    board.setwarnings(False)
    board.setmode(board.BOARD)
    board.setup(12, board.OUT)

def set_LED_status(status):
    if status:
        board.output(11, board.HIGH)
    else:
        board.output(11, board.LOW)

class HardwareController:
    def __init__(self, hardware_queue, message_queue):
        self.hardware_model = message_model._HardwareModel()

        setup_GPIO()

        while True:
            if not hardware_queue.empty():
                self.hardware_model.LED = hardware_queue.get(block=False).LED

            set_LED_status(self.hardware_model.LED)

def run(hardware_queue, message_queue):
    controller = HardwareController(hardware_queue=hardware_queue, message_queue=message_queue)