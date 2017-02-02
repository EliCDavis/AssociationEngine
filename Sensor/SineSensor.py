import math
from Sensor import *

class SineSensor():
    def __init__(self):
        self.wave = []

    def sine_wave(self):
        given = Sensor()
        for angle in range(given.data_feed):
            x = math.sin(math.radians(angle))
            self.wave.append(x)
        return self.wave

test_one = SineSensor()

#Output Test
print(test_one.sine_wave())
