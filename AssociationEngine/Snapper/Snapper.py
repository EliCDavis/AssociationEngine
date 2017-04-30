class Snapper:
    def __init__(self, manager=None, time_window=10):
        self.sensors = []
        self.dataBuffer = {}
        self.snapshot = {}
        self.manager = manager
        self.timeWindow = time_window
        self.windowStart = None
        self.windowEnd = None

    def set_window_size(self, new_window_size):
        # Should just set the window size and let it take effect on next
        # snapshot
        self.timeWindow = new_window_size

    def on_data(self, sensor, data, timestamp=None):
        """
        This function receives data from a sensor and stores it for use in
        snapshot building.

        :param sensor:
        :param data:
        :param timestamp:
        :return:
        """
        # Initialize time window if it is not properly initialized.
        if (self.windowStart is None) and (timestamp is not None):
            self.windowStart = timestamp
            self.windowEnd = self.windowStart + self.timeWindow - 1

        # Create and push a snapshot once window is filled.
        if timestamp > self.windowEnd:

            self.create_snapshot()

            if self.manager is not None:
                self.forward_snapshot()

            self.dataBuffer[sensor.uuid] = [data]

        elif timestamp >= self.windowStart:
            if self.dataBuffer[sensor.uuid] is None:
                self.dataBuffer[sensor.uuid] = [data]
            else:
                self.dataBuffer[sensor.uuid].append(data)

    def add_sensor(self, sensor):
        """
        This function adds a new sensor to the snapper module.

        :return:
        """
        self.sensors.append(sensor)
        self.dataBuffer[sensor.uuid] = None
        sensor.set_snapper_callback(self)

    def remove_sensor(self, sensor):
        """
        This function removes an old sensor from the snapper module.

        :return:
        """
        self.dataBuffer.pop(sensor.uuid, None)
        self.snapshot.pop(sensor.uuid, None)
        self.sensors.remove(sensor)

    def create_snapshot(self):
        """
        This function collects all available data and builds the newest
        snapshot of synchronized values.

        :return:
        """

        # Construct actual snapshot
        self.snapshot["start"] = self.windowStart
        self.snapshot["end"] = self.windowEnd
        for each in self.sensors:
            if self.dataBuffer[each.uuid] is not None:
                self.snapshot[each.uuid] = sum(self.dataBuffer[each.uuid]) / \
                                           len(self.dataBuffer[each.uuid])
            else:
                self.snapshot[each.uuid] = None
            # Clean buffer as we go
            self.dataBuffer[each.uuid] = None

        # Clean buffer and move window for next snapshot operation
        self.windowStart = self.windowEnd
        self.windowEnd = self.windowStart + self.timeWindow - 1

    def get_snapshot(self):
        """
        This function returns the current snapshot on request.

        :return:
        """
        self.create_snapshot()

        return self.snapshot

    def forward_snapshot(self):
        """
        Forwards/publishes the snapshot to the manager for further process.

        :return:
        """
        self.manager.on_data(self.snapshot)
