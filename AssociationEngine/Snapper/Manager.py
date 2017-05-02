from AssociationEngine.Relationship.SpearframeRelationship \
    import SpearframeRelationship
from AssociationEngine.Relationship.Variable import Variable
from AssociationEngine.Snapper.Snapper import Snapper

from AssociationEngine.Snapper.AssociationMatrix import AssociationMatrix


class Manager:

    def __init__(self):
        self.sensors = []
        self.route_map = {}
        self.reverse_route_map = {}
        self.variables = []
        self.snapper = Snapper(self)
        self.matrix = AssociationMatrix()

    def set_window_size(self, new_window_size):
        self.snapper.set_window_size(new_window_size)

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
        self.reverse_route_map[str(newVariable.uuid)] = sensor.uuid


    def remove_sensor(self, sensor):
        """
        This function removes a new sensor to the snapper module, removes
        variable from manager, and removes the corresponding relationships
        from the matrix.

        :return:
        """
        variable = self.route_map[sensor.uuid]
        self.route_map.pop(sensor.uuid)
        self.reverse_route_map.pop(str(variable.uuid))

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

    def get_relationships_by_value_range(self, minvalue, maxvalue):
        """
        Returns the underlying matrix on demand.

        :return:
        """
        return self.matrix.get_relationships_by_value_range(minvalue, maxvalue)

    def on_data(self, snapshot):
        """
        Routes all data from incoming snapshot to the appropriate variables.

        :param snapshot:
        :return:
        """
        start = snapshot.pop("start")
        stop = snapshot.pop("end")
        for sensorID in snapshot:
            variable = self.route_map[sensorID]
            value = snapshot[sensorID]
            variable.on_data(value, start, stop)

    def get_relationship_from_sensors(self, sensor1, sensor2):
        return self.matrix.get_relationship_from_sensors(sensor1, sensor2)

    def get_all_relationships(self):
        return self.matrix.relationships
