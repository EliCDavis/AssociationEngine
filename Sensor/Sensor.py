from uuid import uuid4


class Sensor:
    def __init__(self):
        self.snapper = None
        self.uuid = uuid4()

    def publish(self, data):
        if self.snapper is not None:
            self.snapper.on_data(self, data)

    def set_snapper_callback(self, snapper):
        self.snapper = snapper
