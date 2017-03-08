from Snapper.Manager import Manager
from Snapper.Snapper import Snapper
from Snapper.AssociationMatrix import AssociationMatrix
from Sensor.Sensor import Sensor
from Relationship.Variable import Variable


def test_should_initialize_snapper_and_matrix():
    manager = Manager()
    assert isinstance(manager.snapper, Snapper)
    assert isinstance(manager.matrix, AssociationMatrix)


def test_add_and_remove_sensor_variable_pair():
    manager = Manager()
    sensor = Sensor()
    manager.add_sensor(sensor)

    assert manager.sensors == [sensor]
    assert isinstance(manager.variables[0], Variable)

    manager.remove_sensor(sensor)

    assert manager.sensors == []
    assert manager.variables == []


def test_return_matrix():
    manager = Manager()
    matrix = manager.get_matrix()

    assert matrix == manager.matrix
