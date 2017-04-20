import math

from AssociationEngine.Sensor.Sensor import Sensor


class Sine(Sensor):
    def tick(self, time):
        self.publish(math.sin(time), time)
