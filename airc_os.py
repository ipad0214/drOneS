import threading
import websocket
import message_model
import queue
import pip
import time
import os
import hardware_controller
import console_controller


def install_dependencies():
    pip.main("install", )

version = "0.1.1"
cpu_architecture = os.uname()[4][:3]
operating_system = os.uname()[1]
gpio_model = message_model.GpioModel()


def create_welcome_screen():
    print("###################")
    print("#                 #")
    print("#       {}      #".format(console_controller.create_header("LUNA")))
    print("#     v. {}    #".format(version))
    print("#                 #")
    print("###################")
    print("")
    print("cpu architecture: {}".format(cpu_architecture))
    if cpu_architecture != "arm":
        print(">>> no arm architecture, board outputs will be printed.")
    print("operating system: {}".format(operating_system))
    print("booting LUNA")

    logging = Logging()


def main():
    create_welcome_screen()

    q = queue.Queue()
    websocket_queue = queue.Queue()
    arduino_queue = queue.Queue()
    hardware_queue = queue.Queue()

    message_thread = threading.Thread(target=message_model.run, args=(q, websocket_queue, arduino_queue))
    web_thread = threading.Thread(target=websocket.run, args=(q, websocket_queue, hardware_queue, gpio_model))
    hardware_thread = threading.Thread(target=hardware_controller.run, args=(hardware_queue, q,))

    try:
        web_thread.start()
        print("websocket_thread: {}".format(console_controller.ok()))
    except:
        print("websocket_thread: {}".format(console_controller.failed()))
        pass

    try:
        hardware_thread.start()
        print("hardware_thread: {}".format(console_controller.ok()))
    except:
        print("hardware_thread: {}".format(console_controller.failed()))
        pass

    try:
        message_thread.start()
        print("message_thread: {}".format(console_controller.ok()))
    except:
        print("message_thread: {}".format(console_controller.failed()))
        pass

    print("luna os boot complete")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()

