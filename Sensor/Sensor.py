class Sensor():

    def __init__(self, snapper):
        self.snapper = snapper
    
    def Publish(self, data):
        self.snapper.onData(self, data)
        

