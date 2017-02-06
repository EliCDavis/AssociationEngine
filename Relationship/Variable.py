class Variable:

    def __init__(self):
        self.__class__ == 'Variable'
        self.lastValue = 0.0
        self.subscribers = []

    def onData(self, snapshot):
        return

    def display(self, sensor, value):
        return