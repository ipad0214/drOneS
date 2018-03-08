import json


class GpioModel:
    def __init__(self):
        self.websocket_led = False
        self.websocket_receive_led = False
        self.websocket_send_led = False


class MessageModel:
    def __init__(self):
        self.November = _EngineModel()
        self.Echo = _EngineModel()
        self.Sierra = _EngineModel()
        self.Whisky = _EngineModel()
        self.Hardware = _HardwareModel()
        self.Gyroscope = _GyroModel()


class _EngineModel:
    def __init__(self):
        self.Value = 0
        self.Status = 0


class _GyroModel:
    def __init__(self):
        self.Pitch = 0
        self.Roll = 0
        self.Yaw = 0


class MessageThread:
    def __init__(self, q, websocket_queue, arduino_queue):
        self.message_model = MessageModel()
        self.q = q
        self.websocket_queue = websocket_queue
        self.arduino_queue = arduino_queue
        #self.hardware_queue = hardware_queue

        while True:
            self.update_model_from_json()
            self.update_model_from_arduino()

    def send_model_as_json(self):
        msg = json.dumps(self.message_model, default=lambda o: o.__dict__,
                           sort_keys=True, indent=4)
        self.websocket_queue.put(msg)

    def update_model_from_arduino(self):
        if not self.arduino_queue.empty():
            values = self.arduino_queue.get(block=False)
            # print(values)
            self.message_model.November.EngineValue = values
            self.send_model_as_json()

    def update_model_from_json(self):
        if not self.q.empty():
            value_object = json.loads(self.q.get(block=False))
            # engines
            self.message_model.Echo.Value = value_object["Echo"]["Value"]
            self.message_model.Echo.Status = value_object["Echo"]["Status"]
            self.message_model.November.Value = value_object["November"]["Value"]
            self.message_model.November.Status = value_object["November"]["Status"]
            self.message_model.Sierra.Value = value_object["Sierra"]["Value"]
            self.message_model.Sierra.Status = value_object["Sierra"]["Status"]
            self.message_model.Whisky.Value = value_object["Whisky"]["Value"]
            self.message_model.Whisky.Status = value_object["Whisky"]["Status"]
            # gyro
            self.message_model.Gyroscope.Pitch = value_object["Gyroscope"]["Pitch"]
            self.message_model.Gyroscope.Roll = value_object["Gyroscope"]["Roll"]
            self.message_model.Gyroscope.Yaw = value_object["Gyroscope"]["Yaw"]

            if self.arduino_queue is not None:
                self.arduino_queue.put(self.message_model)
        else:
            return

        print(self.message_model.Hardware.LED)
