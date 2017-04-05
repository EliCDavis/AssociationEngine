from Snapper.Snapper import Snapper
from Snapper.AssociationMatrix import AssociationMatrix
from Relationship.Variable import Variable
from Relationship.SpearframeRelationship import SpearframeRelationship


class Manager:

    def __init__(self):
        self.sensors = []
        self.route_map = {}
        self.variables = []
        self.snapper = Snapper(self)
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

        for var in self.variables:
            relationship = SpearframeRelationship(newVariable, var)
            self.matrix.add_relationship(relationship)

        self.variables.append(newVariable)
        self.route_map[sensor.uuid] = newVariable

    def remove_sensor(self, sensor):
        """
        This function removes a new sensor to the snapper module, removes
        variable from manager, and removes the corresponding relationships
        from the matrix.

        :return:
        """
        variable = self.route_map[sensor.uuid]
        self.route_map.pop(sensor.uuid)

        for var in self.variables:
            if var == variable:
                pass
            else:
                relationship = SpearframeRelationship(variable, var)
                self.matrix.remove_relationship(relationship)

        self.snapper.remove_sensor(sensor)
        self.sensors.remove(sensor)
        self.variables.remove(variable)

    def get_matrix(self):
        """
        Returns the underlying matrix on demand.

        :return:
        """
        return self.matrix

    def get_value_matrix(self):
        """
        Returns the underlying matrix on demand.

        :return:
        """
        return self.matrix.get_value_matrix()

    def on_data(self, snapshot):
        """
        Routes all data from incoming snapshot to the appropriate variables.

        :param snapshot:
        :return:
        """
        for sensorID in snapshot:
            variable = self.route_map[sensorID]
            value = snapshot[sensorID]
            variable.on_data(value)
