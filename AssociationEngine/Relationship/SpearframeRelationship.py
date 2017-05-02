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

        if not self.__frame_table_exists():
            self.__create_frame_table()

        # Create a frame for keeping up with all previous frames computed
        self.summed_frame = None

        # Current Frame
        self.frame = None

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
        self.current_iteration[self.sensor_x.get_uuid()].clear()
        self.current_iteration[self.sensor_y.get_uuid()].clear()
        self.x_last_direction = 0
        self.y_last_direction = 0
        self.current_frame_start_time += frame.get_total_time()
        return frame

    def __frame_table_exists(self):
        con = sqlite3.connect(self.db_name)
        with con:
            cur = con.cursor()
            exists = cur.execute("SELECT name FROM sqlite_master "
                                 "WHERE type='table' "
                                 "AND name='relationships'").fetchone()
        con.close()
        return exists

    def __create_frame_table(self):
        con = sqlite3.connect(self.db_name)
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE relationships ("
                        + "relationship_uuid TEXT, correlation REAL,"
                        + " start_time INTEGER, end_time INTEGER)")
        con.close()

    def __insert_frame_to_db(self):
        frame_duration = self.frame.get_start_time() + \
                         self.frame.get_total_time()
        con = sqlite3.connect(self.db_name)
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO relationships VALUES (?,?,?,?)",
                        (str(self.uuid),
                         self.frame.get_final_correlation(),
                         self.frame.get_start_time(),
                         frame_duration))
        con.close()

    # Method no longer being used
    # def __get_total_frames(self):
    #     con = sqlite3.connect(self.db_name)
    #     with con:
    #         cur = con.cursor()
    #         total = cur.execute("SELECT COUNT(*) "
    #                             "FROM relationships").fetchone()[0]
    #     con.close()
    #     return total

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

        if start_time < self.current_frame_start_time:
            return

        if value is not None:
            # Update our current iteration
            self.current_iteration[id_of_var].append(value)

            # If we've generated
            if self.__should_generate_new_frame(
                    self.current_iteration[self.sensor_x.get_uuid()],
                    self.current_iteration[self.sensor_y.get_uuid()]):
                self.frame = self.__generate_frame_from_values(
                    self.current_iteration[self.sensor_x.get_uuid()],
                    self.current_iteration[self.sensor_y.get_uuid()])
                if self.summed_frame is None:
                    association = generate_association([self.frame])
                    self.summed_frame = self.frame
                else:
                    association = generate_association(
                                    [self.summed_frame, self.frame])
                    self.summed_frame.final_correlation = association
                    frame_time = self.frame.get_total_time()
                    self.summed_frame.total_time += frame_time
                self._push_to_subscribers(association)
                self.__insert_frame_to_db()
        else:
            self.current_frame_start_time = end_time
            self.x_mono_list.clear()
            self.y_mono_list.clear()
            self.current_iteration[self.sensor_x.get_uuid()].clear()
            self.current_iteration[self.sensor_y.get_uuid()].clear()
            self.x_last_direction = 0
            self.y_last_direction = 0

    def get_correlation_coefficient(self):
        if self.get_last_pushed_value() is None:
            return 0.0
        elif not self.current_iteration[self.sensor_x.get_uuid()] \
                and not self.current_iteration[self.sensor_y.get_uuid()]:
            return self.get_last_pushed_value()
        else:
            frame = Frame(self.current_frame_start_time)

            x_vals = self.current_iteration[self.sensor_x.get_uuid()]
            y_vals = self.current_iteration[self.sensor_y.get_uuid()]

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

            if frame.get_final_correlation() is not None:
                current_iter_association = generate_association([frame])
                current_iter_time = frame.get_total_time()
                total_iter_time = self.summed_frame.get_total_time()

                current_iter_ratio = current_iter_time / \
                    (current_iter_time + total_iter_time)
                total_iter_ratio = total_iter_time / \
                    (current_iter_time + total_iter_time)

                current_iter = current_iter_association * current_iter_ratio
                total_iter = self.get_last_pushed_value() * total_iter_ratio

                return current_iter + total_iter
            else:
                return self.get_last_pushed_value()

    def get_value_between_times(self, start_time, end_time):
        con = sqlite3.connect(self.db_name)
        with con:
            cur = con.cursor()
            frames = cur.execute(
                'SELECT * FROM relationships '
                'WHERE end_time >= ? AND start_time < ?',
                (start_time, end_time)).fetchall()

        summed_association = 0.0
        duration = end_time - start_time
        end_index = 3
        correlation_index = 1
        for frame in frames:
            if frame[end_index] > end_time:
                frame_end = end_time
            else:
                frame_end = frame[end_index]
            ratio = (frame_end - start_time) / duration
            summed_association += ratio * abs(frame[correlation_index])
            start_time = frame_end

        con.close()

        return summed_association

    # def __del__(self):
    #     print("Connection closed", self.tempid)
    #     self.db_cursor.close()
    #     self.connection.close()

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
