import threading
import websocket
import message_model
import queue
import time

from random import randint


def main():
    q = queue.Queue()
    websocket_queue = queue.Queue()
    arduino_queue = queue.Queue()
    message_thread = threading.Thread(target=message_model.MessageThread, args=(q, websocket_queue, arduino_queue, ))
    web_thread = threading.Thread(target=websocket.run, args=(q, websocket_queue,))
    web_thread.start()
    message_thread.start()

    while True:
        time.sleep(1)
        arduino_queue.put(randint(0, 100))



if __name__ == "__main__":
    main()

