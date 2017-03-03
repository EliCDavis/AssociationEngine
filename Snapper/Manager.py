from Relationship.Variable import Variable
from Snapper.Snapper import Snapper


class Manager:

    def __init__(self):
        self.sensors = []
        self.dataBuffer = {}
        self.routeMap = {}
        self.variables = []
        self.snapper = Snapper()

    def add_sensor(self):
        pass

    def remove_sensor(self):
        pass

    def get_matrix(self):
        pass
