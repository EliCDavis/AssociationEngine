import math
from Sensor import *

class CosineSensor():
    def __init__(self):
        self.wave = []

    def cosine_wave(self):
        given = Sensor()
        for angle in range(given.data_feed):
            x = math.cos(math.radians(angle))
            self.wave.append(x)
        return self.wave

test_one = CosineSensor()

#Output Test
print(test_one.cosine_wave())
