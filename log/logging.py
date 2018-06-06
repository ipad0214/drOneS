import os

class Logging:
    def __init__(self):
        if not os.path.exists("log.txt"):
            self.log = open("log.txt", "w")
        else:
            self.log = open("log.txt")

    def create_log_entry(self, module, status, message):
        msg = "MODULE: {0} - STATUS: {1} - MESSAGE: {2}".format(module, status, message)
        self.log.write(msg)