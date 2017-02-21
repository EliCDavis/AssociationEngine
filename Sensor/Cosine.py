from Sensor.Sensor import *
import math

class Cosine(Sensor):

    def tick(self, time):
        self.Publish(math.cos(time))
