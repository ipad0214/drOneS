import tornado.web
import tornado.websocket
import message_model
import tornado.ioloop
import threading

websocket_port = 7004
connections = []


# WebSocket server tornado <-> WebInterface
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    def initialize(self, queue, cons, hardware_queue):
        self.hardware_model = message_model.GpioModel()
        self.queue = queue
        self.connections = cons
        self.hardware_queue = hardware_queue

        if self.hardware_queue is not None:
            self.hardware_queue.put()

    # the client connected
    def check_origin(self, origin):
        return True

    def open(self):
        print("New client connected")
        self.connections.append(self)

    # the client sent the message
    def on_message(self, message):
        self.queue.put(message)

    # client disconnected
    def on_close(self):
        print("Client disconnected")
        self.connections.remove(self)


def send(queue):
    while True:
        if not queue.empty():
            for ws in connections:
                ws.write_message(queue.get())


def run(queue, websocket_queue, hardware_queue=None):
    send_thread = threading.Thread(target=send, args=(websocket_queue, ))
    send_thread.start()
    application = tornado.web.Application([
        (r"/", WebSocketHandler, dict(queue=queue, cons=connections, hardware_queue=hardware_queue))
    ])

    application.listen(websocket_port)
    tornado.ioloop.IOLoop.instance().start()
