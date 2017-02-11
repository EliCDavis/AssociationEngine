class Snapper:
    def __init__(self):
        self.sensors = []
        self.snapshot = []
        self.startTime = 0.0
        self.variables = []

    def step(self):
        """
        runs next incremental step in building a snapshot.
        :return:
        """
        pass

    def on_data(self, sensor, data):
        """
        This function receives data from a sensor and stores it for use in snapshot building.
        :param sensor:
        :param data:
        :return:
        """
        pass

    def create_snapshot(self):
        """
        This function collects all available data and builds the newest snapshot of synchronized values.
        :return:
        """
        pass

    def forward_snapshot(self):
        """
        This function forwards data to variables in the relationship builder module.
        :return:
        """
        for variable in self.variables:
            variable.onData(snapshot[variable.uuid])
