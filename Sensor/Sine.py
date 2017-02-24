from Sensor.Sensor import Sensor
import math


class Sine(Sensor):
    def tick(self, time):
        self.Publish(math.sin(time))
