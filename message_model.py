import json
import console_controller


class GpioModel:
    def __init__(self):
        self.websocket_led = False
        self.websocket_receiving_led = False
        self.websocket_sending_led = False


class MessageModel:
    def __init__(self):
        self.November = _EngineModel()
        self.Echo = _EngineModel()
        self.Sierra = _EngineModel()
        self.Whisky = _EngineModel()
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
            self.update_if_newer("Echo", "Value", value_object["Echo"]["Value"])
            self.update_if_newer("Echo", "Status", value_object["Echo"]["Status"])
            
            self.update_if_newer("November", "Value", value_object["November"]["Value"])
            self.update_if_newer("November", "Status", value_object["November"]["Status"])
            
            self.update_if_newer("Sierra", "Value", value_object["Sierra"]["Value"])
            self.update_if_newer("Sierra", "Status", value_object["Sierra"]["Status"])
            
            self.update_if_newer("Whisky", "Value", value_object["Whisky"]["Value"])
            self.update_if_newer("Whisky", "Status", value_object["Whisky"]["Status"])
            
            # gyro
            self.update_if_newer("Gyroscope", "Pitch", value_object["Gyroscope"]["Pitch"])
            self.update_if_newer("Gyroscope", "Yaw", value_object["Gyroscope"]["Yaw"])
            self.update_if_newer("Gyroscope", "Roll", value_object["Gyroscope"]["Roll"])
        else:
            return
        
    def update_if_newer(self, name, datapoint, value):
        current_value = getattr(getattr(self.message_model, name), datapoint)
        if current_value != value:
            setattr(getattr(self.message_model, name), datapoint, value)
            self.arduino_queue.put(self.create_update_message(name, datapoint, value))
            console_controller.create_message_event_info(datapoint, name, current_value, getattr(getattr(self.message_model, name)))

            
    def create_update_message(self, name, datapoint, value):
        return "0101{}".format(value)


def run(q, websocket_queue, arduino_queue):
    controller = MessageThread(q=q, websocket_queue=websocket_queue, arduino_queue=arduino_queue)
