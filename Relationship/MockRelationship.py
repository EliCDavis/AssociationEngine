from Relationship.Relationship import Relationship


class MockRelationship(Relationship):
    """
    Mock class to be used for testing.
    """

    def __init__(self, sensor_x, sensor_y):
        """
        A Relationship takes two sensors and subscribes to them for computation
        :type sensor_y: Variable
        :type sensor_x: Variable
        """

        # set up our parent class
        Relationship.__init__(self, sensor_x, sensor_y)

        self.correlation_coefficient = None

    def get_correlation_coefficient(self):
        return self.correlation_coefficient

    def set_correlation_coefficient(self, value):
        self.correlation_coefficient = value
