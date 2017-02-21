from ..Relationship.Variable import Variable


class Snapper:
    def __init__(self):
        self.sensors = []
        self.dataBuffer = {}
        self.routeMap = {}
        self.snapshot = {}
        self.startTime = 0.0
        self.variables = []

    def step(self):
        """
        runs next incremental step in building a snapshot.
        :return:
        """
        pass

    def onData(self, sensor, data):
        """
        This function receives data from a sensor and stores it for use in snapshot building.
        :param sensor:
        :param data:
        :return:
        """
        self.dataBuffer[sensor.uuid] = data

    def add_sensor(self, sensor):
        self.sensors.append(sensor)
        newVariable = Variable()
        self.variables.append(newVariable)
        self.routeMap[sensor.uuid] = newVariable.uuid

    def create_snapshot(self):
        """
        This function collects all available data and builds the newest snapshot of synchronized values.
        :return:
        """
        for sensor in self.dataBuffer:
            self.snapshot[self.routeMap[sensor]] = self.dataBuffer[sensor]

    def forward_snapshot(self):
        """
        This function forwards data to variables in the relationship builder module.
        :return:
        """
        for variable in self.variables:
            variable.onData(self.snapshot[variable.uuid])
