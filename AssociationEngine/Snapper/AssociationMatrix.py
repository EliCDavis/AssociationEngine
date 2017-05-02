class AssociationMatrix:
    def __init__(self):
        self.relationships = {}

    def add_relationship(self, relationship):
        a = (relationship.sensor_x.get_uuid(),
             relationship.sensor_y.get_uuid())
        self.relationships[frozenset(a)] = relationship
        return

    def remove_relationship(self, relationship):
        """Removing relationships could be different depending
            on who is doing the removing. If another module does
            it the relationship_id could be used. If the end-user
            is removing them then it will need to be searched
            by a pair of sensors.
        """
        a = (relationship.sensor_x.get_uuid(),
             relationship.sensor_y.get_uuid())
        self.relationships.pop(frozenset(a), None)
        return

    def get_value_matrix(self):
        dict_with_values = {}
        for key, value in self.relationships.items():
            dict_with_values[key] = value.get_correlation_coefficient()
        return dict_with_values

    def get_relationships_by_value_range(self, minvalue, maxvalue):
        sensor_pairs = {}
        for key, value in self.relationships.items():
            if minvalue <= value.get_correlation_coefficient() <= maxvalue:
                sensor_pairs[key] = value.get_correlation_coefficient()
        return sensor_pairs

    def get_relationship_from_sensors(self, sensor1, sensor2):
        a = (sensor1.get_uuid(), sensor2.get_uuid())
        key = frozenset(a)

        return self.relationships[key]
