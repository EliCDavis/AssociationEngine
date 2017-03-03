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

    def on_new_association_value(self, value):
        return

    def get_all_relationships(self):
        dict_with_values = {}
        for key, value in self.relationships.items():
                dict_with_values[key] = value.get_correlation_coefficient()
        return dict_with_values

    def get_single_relationship(self, sensorpair):
        """I need to know who will call this and how, i.e. end
            user with 2 sensor ids or
            sensor_id->sensor_uuid->frozenset.
        """
        pass

    def get_relationships_by_value_range(self, minvalue, maxvalue):
        sensor_pairs = {}
        for key, value in self.relationships.items():
            if minvalue <= value.get_correlation_coefficient() <= maxvalue:
                sensor_pairs[key] = value.get_correlation_coefficient()
        return sensor_pairs

    def get_relationship_by_time_range(self):
        """
        Requires Realationship functions to implement.
        """
        pass

    def display(self, sensor, value):
        pass
