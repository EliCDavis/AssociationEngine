from scipy.stats import spearmanr
from AssociationEngine.Relationship.Relationship import Relationship
from AssociationEngine.Relationship.Frame import Frame
import sqlite3
import math
import os


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

        # The current aggregation of variable values before a new frame has
        # been generated
        self.current_iteration = {sensor_x.get_uuid(): [],
                                  sensor_y.get_uuid(): []}

        self.db_name = "spearframe.db"
        self.connection = sqlite3.connect(self.db_name)
        self.db_cursor = self.connection.cursor()
        if not self.__frame_table_exists():
            self.__create_frame_table()

        # Create list for keeping up with all previous frames computed
        self.frames = []

        self.x_last_direction = 0
        self.y_last_direction = 0

        # set up our parent class
        Relationship.__init__(self, sensor_x, sensor_y)

        # sensor_x
        self.x_mono_list = []

        # sensor_y
        self.y_mono_list = []

        self.current_frame_start_time = None

    def __should_generate_new_frame(self, x_vals, y_vals):

        if len(x_vals) == 2 and len(y_vals) == 2:
            self.x_last_direction = get_current_direction(
                x_vals[-2], x_vals[-1], self.x_last_direction)
            self.y_last_direction = get_current_direction(
                y_vals[-2], y_vals[-1], self.y_last_direction)
            return False

        if len(x_vals) == len(y_vals) and len(x_vals) > 2:

            x_current_direction = get_current_direction(
                x_vals[-2], x_vals[-1], self.x_last_direction)
            y_current_direction = get_current_direction(
                y_vals[-2], y_vals[-1], self.y_last_direction)

            if self.x_last_direction != x_current_direction \
                    and self.x_last_direction != 0:
                self.x_mono_list.append(len(x_vals) - 2)
            if self.y_last_direction != y_current_direction \
                    and self.y_last_direction != 0:
                self.y_mono_list.append(len(y_vals) - 2)

            self.x_last_direction = x_current_direction
            self.y_last_direction = y_current_direction

            return len(self.x_mono_list) > 0 and len(self.y_mono_list) > 0

    def __generate_frame_from_values(self, x_vals, y_vals):

        frame = Frame(self.current_frame_start_time)

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

        # Reset values..
        self.x_mono_list.clear()
        self.y_mono_list.clear()
        self.x_last_direction = 0
        self.y_last_direction = 0
        self.current_frame_start_time += frame.get_total_time()
        return frame

    def __frame_table_exists(self):
        self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='relationships'")
        return self.db_cursor.fetchone()

    def __create_frame_table(self):
        self.db_cursor.execute("CREATE TABLE relationships ("
                               + "relationship_uuid TEXT, association REAL,"
                               + " start_time INTEGER, end_time INTEGER)")
        self.connection.commit()

    def __insert_frames_to_db(self):
        db_rows = []
        for frame in self.frames:
            db_rows.append((str(self.uuid), frame.get_final_correlation(),
                            frame.get_start_time(),
                            frame.get_start_time() + frame.get_total_time()))
        self.db_cursor.executemany("INSERT INTO relationships VALUES (?,?,?,?)", db_rows)
        self.connection.commit()
        self.frames = []

    def __get_total_frames(self):
        self.db_cursor.execute("SELECT COUNT(*) FROM relationships")
        return self.db_cursor.fetchone()

    def on_new_value(self, value, id_of_var, start_time, end_time):

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

        if self.current_frame_start_time is None:
            self.current_frame_start_time = start_time

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
            self.__insert_frames_to_db()

    def get_correlation_coefficient(self):
        if not self.frames:
            return self.get_last_pushed_value()
        else:
            current_iter_association = generate_association(self.frames)
            current_iter_frame_count = len(self.frames)
            total_frame_count = self.__get_total_frames()

            current_iter_ratio = current_iter_frame_count / \
                (current_iter_frame_count + total_frame_count)
            total_iter_ratio = total_frame_count / \
                (current_iter_frame_count + total_frame_count)

            current_iter = current_iter_association * current_iter_ratio
            total_iter = self.get_last_pushed_value() * total_iter_ratio

            return current_iter + total_iter

    def get_value_between_times(self, start_time, end_time):
        self.db_cursor.execute(
            'SELECT * FROM relationships '
            'WHERE end_time >= ? AND start_time < ?',
            (start_time, end_time))

        frames = self.db_cursor.fetchall()

        summed_association = 0
        duration = end_time - start_time
        for frame in frames:
            if frame['end_time'] > end_time:
                frame_end = end_time
            else:
                frame_end = frame['end_time']
            association = (frame_end - start_time) / duration
            summed_association += association * frame['association']
            start_time = frame_end

        return summed_association

    def __del__(self):
        self.connection.close()

    def clean_up(self):
        os.remove(self.db_name)


def get_current_direction(x, y, last):
    """
    Determines whether or not a change in direction
    of two points and last direction.
    Returns last if a change has not occurred.
    Returns 1 if a change has occurred and last is not 1
    Returns -1 if a change has occurred and last is not -1
    :param x:
    :param y:
    :param last:
    :return:
    """
    if x == y:
        return last

    if y-x > 0:
        return 1

    return -1


def generate_association(frames):
    """
    Generates a numerical value (0-1) which describes how strongly two
    variables are associated with one another given a list of non empty
    Frame objects

    :type frames: list:Frame
    """
    gen_assoc = sum(
        list(
            map(
                lambda x: x.get_total_time() * abs(x.get_final_correlation()),
                frames
            )
        )
    ) / sum(list(map(lambda x: x.get_total_time(), frames)))

    return 0 if math.isnan(gen_assoc) else gen_assoc
