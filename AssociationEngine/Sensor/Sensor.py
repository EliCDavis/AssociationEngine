from uuid import uuid4
from time import time


class Sensor:
    def __init__(self):
        self.snapper = None
        self.uuid = uuid4()

    def publish(self, data, timestamp=time()):
        if self.snapper is not None:
            self.snapper.on_data(self, data, timestamp)

    def set_snapper_callback(self, snapper):
        self.snapper = snapper
