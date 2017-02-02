class Sensor:

    def __init__(self):
        self.snapper = Snapper()
    
    def Publish(self, data):
        self.snapper.onData(self, data)
        

