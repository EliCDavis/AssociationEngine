from Snapper.Snapper import Snapper
from Snapper.AssociationMatrix import AssociationMatrix
from Relationship.Variable import Variable


class Manager:

    def __init__(self):
        self.sensors = []
        self.route_map = {}
        self.variables = []
        self.snapper = Snapper()
        self.matrix = AssociationMatrix()

    def add_sensor(self, sensor):
        """
        This function adds a new sensor to the snapper module and generates
        a corresponding variable object with mappings.

        :return:
        """
        self.sensors.append(sensor)
        self.snapper.add_sensor(sensor)
        newVariable = Variable()
        self.variables.append(newVariable)
        self.route_map[sensor.uuid] = newVariable

    def remove_sensor(self, sensor):
        variable = self.route_map[sensor.uuid]
        self.route_map.pop(sensor.uuid)

        self.snapper.remove_sensor(sensor)
        self.sensors.remove(sensor)
        self.variables.remove(variable)

    def get_matrix(self):
        return self.matrix
