from uuid import uuid4


class Sensor:
    def __init__(self, snapper):
        self.snapper = snapper
        self.uuid = uuid4()

    def publish(self, data):
        self.snapper.on_data(self, data)
