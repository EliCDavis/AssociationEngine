from Relationship.Relationship import Relationship
from Examples.webpage.Server import update_relationship


class Relationship_Subscriber:
    def __init__(self, sensor_x, sensor_y):
        self.relationship = Relationship(sensor_x, sensor_y)
        self.relationship.subscribe(self)

        self.sensor_x = sensor_x
        self.sensor_y = sensor_y

    def on_data(self, value):
        update_relationship(self.sensor_x, self.sensor_y, value)
