from .Relationship import Relationship
from.Variable import Variable


class SpearframeRelationship(Relationship):

    def __init__(self, sensor_x, sensor_y):
        """

        :type sensor_y: Variable
        :type sensor_x: Variable
        """

        # The current aggregation of veriable values before a new frame has been generated
        self.current_iteration = {sensor_x.get_uuid(): [], sensor_y.get_uuid(): []}

        # Create list for keeping up with all previous frames computed
        self.frames = []

        # set up our parent class
        Relationship.__init__(self, sensor_x, sensor_y)

    def __should_generate_new_frame(self, x_vals, y_vals):

        # Make sure their equal in length before going further
        if len(x_vals) != len(y_vals):
            return False

    def __generate_frame_from_values(self, x_vals, y_vals):

        return None

    def on_new_value(self, value, id_of_var):
        """
        This method is called by the variables it is subscribed to, updating the
        relationship on it's newest value.

        :type id_of_var: uuid4
        :type value: float
        """

        # Make sure the value comes from one of our sensors
        if id_of_var not in self.current_iteration:
            raise ValueError("Illegal id: Relationship should not have been pushed this value")

        # Update our current iteration
        self.current_iteration[id_of_var].append(value)

        # If we've generated
        if self.__should_generate_new_frame(self.current_iteration[self.sensor_x.get_uuid()], self.current_iteration[self.sensor_y.get_uuid()]):
            self.frames.append(self.__generate_frame_from_values(self.current_iteration[self.sensor_x.get_uuid()],self.current_iteration[self.sensor_y.get_uuid()]))
