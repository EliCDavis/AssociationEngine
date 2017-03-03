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
        """
        This function adds a new sensor to the snapper module and generates
        a corresponding variable object.

        :return:
        """
        self.sensors.append(sensor)
        newVariable = Variable()
        self.variables.append(newVariable)
        self.routeMap[sensor.uuid] = newVariable.uuid

    def remove_sensor(self):
        pass

    def get_matrix(self):
        pass
