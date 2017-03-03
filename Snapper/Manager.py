from Snapper.Snapper import Snapper
from Snapper.AssociationMatrix import AssociationMatrix


class Manager:

    def __init__(self):
        self.sensors = []
        self.dataBuffer = {}
        self.routeMap = {}
        self.variables = []
        self.snapper = Snapper()
        self.matrix = AssociationMatrix()

    def add_sensor(self):
        pass

    def remove_sensor(self):
        pass

    def get_matrix(self):
        pass
