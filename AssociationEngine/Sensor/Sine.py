import math

from AssociationEngine.Sensor.Sensor import Sensor


class Sine(Sensor):
    def tick(self, time):
        self.Publish(math.sin(time))
