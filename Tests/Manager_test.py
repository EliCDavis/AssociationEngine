from Snapper.Manager import Manager
from Snapper.Snapper import Snapper
from Snapper.AssociationMatrix import AssociationMatrix
from Sensor.Sensor import Sensor
from Relationship.Variable import Variable


def test_should_initialize_object():
    manager = Manager()
    assert isinstance(manager, Manager)


def test_should_initialize_snapper_and_matrix():
    manager = Manager()
    assert isinstance(manager.snapper, Snapper)
    assert isinstance(manager.matrix, AssociationMatrix)


def test_add_and_remove_sensor_variable_pair():
    manager = Manager()
    sensor = Sensor(manager.snapper)
    manager.add_sensor(sensor)

    assert isinstance(manager.sensors[0], Sensor)
    assert isinstance(manager.variables[0], Variable)

    manager.remove_sensor(sensor)

    assert len(manager.sensors) is 0
    assert len(manager.variables) is 0

def test_return_matrix():
    manager = Manager()
    matrix = manager.get_matrix()

    assert isinstance(matrix, AssociationMatrix)
