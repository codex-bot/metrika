from config import COLLECTIONS

class EventBase:

    def __init__(self, sdk):
        self.sdk = sdk
        self.COLLECTIONS = COLLECTIONS
