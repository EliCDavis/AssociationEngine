from uuid import uuid4


class Sensor():

    def __init__(self, snapper):
        self.snapper = snapper
        self.uuid = uuid4()
    
    def Publish(self, data):
        self.snapper.onData(self, data)
        

