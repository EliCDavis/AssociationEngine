from scipy.stats import spearmanr
from .Relationship import Relationship
from .Frame import Frame


class SpearframeRelationship(Relationship):
    """Home grown implementation for determining associtations between sensors

    The spearframe algorithm attempts to break up the 2 streams of variables
    into frames that capture monotonic trends, and then averages out the
    correlations of those variables.
    """

    def __init__(self, sensor_x, sensor_y):
        """
        A Relationship takes two sensors and subscribes to them for computation
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

        # This needs to be replaced with spearframe implementation
        return len(x_vals) >= 10


    def __generate_frame_from_values(self, x_vals, y_vals):

        frame = Frame()
        frame.add_correlation(len(x_vals), spearmanr(x_vals, y_vals)[0])

        return frame

    def __generate_association(self, frames):
        return sum(
            list(
                map(
                    lambda x: x.get_total_time() * abs(x.get_final_correlation()),
                    frames
                    )
                )
            ) / sum(list(map(lambda x: x.get_total_time(), frames)))

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
            self.frames.append(self.__generate_frame_from_values(self.current_iteration[self.sensor_x.get_uuid()], self.current_iteration[self.sensor_y.get_uuid()]))
            self._push_to_subscribers(self.__generate_association(self.frames))
