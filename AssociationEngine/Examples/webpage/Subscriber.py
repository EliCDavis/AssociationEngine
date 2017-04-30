from AssociationEngine.Relationship.Relationship import Relationship



class RelationshipSubscriber:
    def __init__(self, sensor_x, sensor_y, cb):
        self.sensor_x = sensor_x
        self.sensor_y = sensor_y
        self.cb = cb

    def on_data(self, value):
      #  from AssociationEngine.Examples.webpage.Server import update_relationship
        self.cb({"sensor_x": str(self.sensor_x),
                                            "sensor_y": str(self.sensor_y),
                                            "value": value})
       # update_relationship(self.sensor_x, self.sensor_y, value, self.io)
