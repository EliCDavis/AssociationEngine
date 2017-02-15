from uuid import uuid4
from .Variable import Variable


class Relationship:

    def __init__(self, sensor_x, sensor_y):
        """

        :type sensor_y: Variable
        :type sensor_x: Variable

        """

        # Assign sensors appropriately
        self.sensor_x = sensor_x
        self.sensor_y = sensor_y

        # Build new uuid
        self.uuid = uuid4()

        # Perform subscriptions after uuid has been assigned
        sensor_x.add_subscriber(self)
        sensor_y.add_subscriber(self)

    def get_uuid(self):
        return self.uuid

    def on_new_value(self, value, id_of_var):
        return

    def get_correlation_coefficient(self):
        return
