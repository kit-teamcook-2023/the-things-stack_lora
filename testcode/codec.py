import base64

class Codec:
    def __init__(self):
        None

    def decode(self, message: str) -> str: # uplink data
        msg_base64 = base64.b64decode(message)
        return msg_base64.decode('ascii')

    def encode(self, message: str) -> str: # downlink data
        msg = message.encode('ascii')
        msg_base64 = base64.b64encode(msg)
        return msg_base64.decode('ascii')