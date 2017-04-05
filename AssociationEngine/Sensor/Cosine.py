import math

from AssociationEngine.Sensor.Sensor import Sensor


class Cosine(Sensor):
    def tick(self, time):
        self.Publish(math.cos(time))
