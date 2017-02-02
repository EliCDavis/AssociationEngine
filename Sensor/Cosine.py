from Sensor import *

class Cosine(Sensor()):

    def tick(self, time):
        self.Publish()
