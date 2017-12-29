import threading
import websocket
import message_model
import queue
import time
import hardware_controller

from random import randint

def main():
    q = queue.Queue()
    websocket_queue = queue.Queue()
    arduino_queue = queue.Queue()
    hardware_queue = queue.Queue()
    hardware_thread = threading.Thread(target=hardware_controller.run, args=(hardware_queue, q, ))
    message_thread = threading.Thread(target=message_model.MessageThread, args=(q, websocket_queue, arduino_queue, hardware_queue, ))
    web_thread = threading.Thread(target=websocket.run, args=(q, websocket_queue,))

    web_thread.start()
    hardware_thread.start()
    message_thread.start()

    while True:
        time.sleep(1)
        arduino_queue.put(randint(0, 100))


if __name__ == "__main__":
    main()

