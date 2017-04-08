from Sensor.Sensor import Sensor
import math


class Sine(Sensor):
    def tick(self, time):
        self.publish(math.sin(time))
