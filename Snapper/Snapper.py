class Snapper:
    def __init__(self):
        self.sensors = []
        self.dataBuffer = {}
        self.snapshot = {}

    def on_data(self, sensor, data):
        """
        This function receives data from a sensor and stores it for use in
        snapshot building.

        :param sensor:
        :param data:
        :return:
        """
        self.dataBuffer[sensor.uuid] = data

    def add_sensor(self, sensor):
        """
        This function adds a new sensor to the snapper module.

        :return:
        """
        self.sensors.append(sensor)

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
        for sensorID in self.dataBuffer:
            self.snapshot[sensorID] = self.dataBuffer[sensorID]

    def get_snapshot(self):
        """
        This function forwards data to variables in the relationship builder
        module.

        :return:
        """
        self.create_snapshot()

        return self.snapshot
