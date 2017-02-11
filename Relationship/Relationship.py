class Relationship:

    def __init__(self, sensor_x, sensor_y):
        self.type = 'Relationship'
        self.sensor_x = sensor_x
        self.sensor_y = sensor_y

    def on_new_value(self, value, id_of_var):
        return

    def get_correlation_coefficient(self):
        return
