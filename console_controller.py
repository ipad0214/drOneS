HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def create_green_word(text):
    return OKGREEN + text + ENDC

def create_red_word(text):
    return FAIL + text + ENDC

def create_header(header):
    return HEADER + header + ENDC

def ok():
    return OKGREEN + "ok" + ENDC

def failed():
    return FAIL + "failed" + ENDC

def create_message_event_info(**kwargs):
    print(create_header("[DATA UPDATE]") + "Datapoint: {} Name: {} Old Value: {} New Value: {}").format(kwargs)
