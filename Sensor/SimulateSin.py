import math

class Sensor():

    def __init__(self):
        self.SineWave = []
        self.CosineWave = []

    def sine(self, given):
        for angle in range(given):
            #Gets the Sine Wave leading up to a certain angle
            x = (math.sin(math.radians(angle)))
            self.SineWave.append(x)
        return self.SineWave

    def cosine(self, given):
        for angle in range(given):
            #Gets the cosine wave leading up to a certain angle
            x = math.cos(math.radians((angle)))
            self.CosineWave.append(x)
        return self.CosineWave

#This part is really just for testing to make sure to output properly
def main():
    sine = Sensor()
    SineInput = sine.sine(360)
    cosine = Sensor()
    CosineInput = cosine.cosine(360)
    print('Sine: ', SineInput, '\n',  'Cosine: ', CosineInput)

main()