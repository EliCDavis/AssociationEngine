from uuid import uuid4


class Relationship:
    """Abstract class to be implemented via different algorithms.

    This class provides programmers the ability to implement their
    own association algorithm into the system in an easy fashion.
    """

    def __init__(self, sensor_x, sensor_y):
        """

        :type sensor_y: Variable
        :type sensor_x: Variable

        """

        # Create list of subscribers that we'll push too
        self.subscribers = []

        # Assign sensors appropriately
        self.sensor_x = sensor_x
        self.sensor_y = sensor_y

        # Build new uuid
        self.uuid = uuid4()

        # Perform subscriptions after uuid has been assigned
        sensor_x.add_subscriber(self)
        sensor_y.add_subscriber(self)

        # Keep up with the last computed association value
        self._last_pushed_value = None

    def get_uuid(self):
        return self.uuid

    def on_new_value(self, value, id_of_var, start_time, end_time):
        raise NotImplementedError("Underlying algorithm should implement this")

    def get_correlation_coefficient(self):
        raise NotImplementedError("Underlying algorithm should implement this")

    def clean_up(self):
        raise NotImplementedError("Underlying algorithm should implement this")

    def get_last_pushed_value(self):
        return self._last_pushed_value

    def get_value_between_times(self, x, y):
        raise NotImplementedError("Underlying algorithm should implement this")

    def subscribe(self, subscriber):
        """Will add the subscriber to internal list for pushing new data

        Assumes all subscribers passed in will have an 'on_data' method
        that the relationship class can push too.
        """
        self.subscribers.append(subscriber)

    def _push_to_subscribers(self, value):
        for subscriber in range(len(self.subscribers)):
            self.subscribers[subscriber].on_data(value)

        self._last_pushed_value = value
