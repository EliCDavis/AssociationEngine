from scipy.stats import spearmanr
from Relationship.Relationship import Relationship
from Relationship.Frame import Frame


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

        # The current aggregation of veriable values before a new frame has
        # been generated
        self.current_iteration = {sensor_x.get_uuid(): [],
                                  sensor_y.get_uuid(): []}

        # Create list for keeping up with all previous frames computed
        self.frames = []

        # set up our parent class
        Relationship.__init__(self, sensor_x, sensor_y)

        # sensor_x
        self.x_mono_list = []

        # sensor_y
        self.y_mono_list = []

    def __should_generate_new_frame(self, x_vals, y_vals):

        # Make sure their equal in length before going further
        if len(x_vals) != len(y_vals) or len(x_vals) < 3:
            return False

        # check both x_vals and y_vals for monotonic changes
        if check_for_monotonic_change(x_vals[-3], x_vals[-2], x_vals[-1]):
            self.x_mono_list.append(len(x_vals) - 2)

        if check_for_monotonic_change(y_vals[-3], y_vals[-2], y_vals[-1]):
            self.y_mono_list.append(len(y_vals) - 2)

        # This needs to be replaced with spearframe implementation
        return len(self.x_mono_list) > 0 and len(self.y_mono_list) > 0

    def __generate_frame_from_values(self, x_vals, y_vals):

        frame = Frame()

        if len(self.x_mono_list) >= len(self.y_mono_list):
            previous_index = 0
            for mono_change_index in self.x_mono_list:
                frame.add_correlation(
                    len(x_vals[previous_index:mono_change_index]),
                    spearmanr(x_vals[previous_index:mono_change_index],
                              y_vals[previous_index:mono_change_index])[0])
                previous_index = mono_change_index
        else:
            previous_index = 0
            for mono_change_index in self.y_mono_list:
                frame.add_correlation(
                    len(x_vals[previous_index:mono_change_index]),
                    spearmanr(x_vals[previous_index:mono_change_index],
                              y_vals[previous_index:mono_change_index])[0])
                previous_index = mono_change_index

        self.x_mono_list.clear()
        self.y_mono_list.clear()

        return frame

    def on_new_value(self, value, id_of_var):
        """
        This method is called by the variables it is subscribed to, updating
        the relationship on it's newest value.

        :type id_of_var: uuid4
        :type value: float
        """

        # Make sure the value comes from one of our sensors
        if id_of_var not in self.current_iteration:
            raise ValueError(
                "Illegal id: Relationship should not have been pushed this "
                "value")

        # Update our current iteration
        self.current_iteration[id_of_var].append(value)

        # If we've generated
        if self.__should_generate_new_frame(
                self.current_iteration[self.sensor_x.get_uuid()],
                self.current_iteration[self.sensor_y.get_uuid()]):
            self.frames.append(self.__generate_frame_from_values(
                self.current_iteration[self.sensor_x.get_uuid()],
                self.current_iteration[self.sensor_y.get_uuid()]))
            self._push_to_subscribers(generate_association(self.frames))


def check_for_monotonic_change(x, y, z):
    """
    Determines whether or not a change in direction as x => y => z has
    occurred. Returns True if a change has occurred
    :param x:
    :param y:
    :param z:
    :return:
    """
    return ((y - x) / abs(y - x)) != ((z - y) / abs(z - y))


def generate_association(frames):
    """
    Generates a numerical value (0-1) which describes how strongly two
    variables are associated with one another given a list of non empty
    Frame objects

    :rtype : float
    :type frames: list:Frame
    """
    return sum(
        list(
            map(
                lambda x: x.get_total_time() * abs(x.get_final_correlation()),
                frames
            )
        )
    ) / sum(list(map(lambda x: x.get_total_time(), frames)))
