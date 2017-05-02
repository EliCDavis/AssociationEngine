from uuid import uuid4
from time import time


class Sensor:
    def __init__(self, name=None):
        self.snapper = None
        self.uuid = uuid4()
        self.name = name

    def publish(self, data, timestamp=time()):
        if self.snapper is not None:
            self.snapper.on_data(self, data, timestamp)

    def set_snapper_callback(self, snapper):
        self.snapper = snapper

    def __str__(self):
        return str(self.uuid) if self.name is None else self.name
