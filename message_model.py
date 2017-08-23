import json

class MessageModel:
    def __init__(self):
        self.November = _EngineModel()
        self.Echo = _EngineModel()
        self.Sierra = _EngineModel()
        self.Whiskey = _EngineModel()
        self.Hardware = _HardwareModel()
        self.Gyroscope = _GyroModel()


class _EngineModel:
    def __init__(self):
        self.EngineValue = 0
        self.EngineStatus = 0


class _HardwareModel:
    def __init__(self):
        self.LED = False


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
            self.message_model.Echo.EngineValue = value_object["Echo"]["EngineValue"]
            self.message_model.Echo.EngineStatus = value_object["Echo"]["EngineStatus"]
            self.message_model.November.EngineValue = value_object["November"]["EngineValue"]
            self.message_model.November.EngineStatus = value_object["November"]["EngineStatus"]
            self.message_model.Sierra.EngineValue = value_object["Sierra"]["EngineValue"]
            self.message_model.Sierra.EngineStatus = value_object["Sierra"]["EngineStatus"]
            self.message_model.Whiskey.EngineValue = value_object["Whiskey"]["EngineValue"]
            self.message_model.Whiskey.EngineStatus = value_object["Whiskey"]["EngineStatus"]
            # hardware
            self.message_model.Hardware.LED = value_object["Hardware"]["Led"]
            # gyro
            self.message_model.Gyroscope.Pitch = value_object["Gyroscope"]["Pitch"]
            self.message_model.Gyroscope.Roll = value_object["Gyroscope"]["Roll"]
            self.message_model.Gyroscope.Yaw = value_object["Gyroscope"]["Yaw"]
        else:
            return

        print(self.message_model.Hardware.LED)
