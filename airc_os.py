import threading
import websocket
import message_model
import queue
import time
import os
import hardware_controller
from random import randint


if not os.uname()[4][:3] == 'arm':
    print("ERROR: NOT RUNNING ON PI => NO GPIO OUTPUT")


def running_on_pi():
    return os.uname()[4][:3] == 'arm'


def main():
    q = queue.Queue()
    websocket_queue = queue.Queue()
    arduino_queue = queue.Queue()
    hardware_queue = queue.Queue()

    message_thread = threading.Thread(target=message_model.run, args=(q, websocket_queue, arduino_queue, hardware_queue))
    web_thread = threading.Thread(target=websocket.run, args=(q, websocket_queue, hardware_queue))
    hardware_thread = threading.Thread(target=hardware_controller.run, args=(hardware_queue, q,))

    web_thread.start()
    hardware_thread.start()
    message_thread.start()

    while True:
        time.sleep(1)
        arduino_queue.put(randint(0, 100))


if __name__ == "__main__":
    main()

