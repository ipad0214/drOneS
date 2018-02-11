import threading
import websocket
import message_model
import arduino_bridge
import queue
import time
import os

if os.uname()[4][:3] == 'arm':
    import hardware_controller
else:
    print("ERROR: NOT RUNNING ON PI => NO GPIO OUTPUT")

def running_on_pi():
    return os.uname()[4][:3] == 'arm'

def main():
    if running_on_pi():
        print("THIS IS A PI!")
    q = queue.Queue()
    websocket_queue = queue.Queue()
    arduino_queue = queue.Queue()
    if running_on_pi():
        hardware_queue = queue.Queue()
        arduino_thread = threading.Thread(target=arduino_bridge.ArduinoBridgeThread, args=(q, arduino_queue, hardware_queue))
        #hardware_thread = threading.Thread(target=hardware_controller.run, args=(hardware_queue, q, ))
        message_thread = threading.Thread(target=message_model.MessageThread,
                                          args=(q, websocket_queue, arduino_queue ))
    else:
        message_thread = threading.Thread(target=message_model.MessageThread, args=(q, websocket_queue, arduino_queue ))

    web_thread = threading.Thread(target=websocket.run, args=(q, websocket_queue,))

    web_thread.start()
    if running_on_pi():
        #hardware_thread.start()
        arduino_thread.start()
    message_thread.start()


    while True:
        time.sleep(1)
        #arduino_queue.put(randint(0, 100))


if __name__ == "__main__":
    main()

