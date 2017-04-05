from Snapper.Manager import Manager
from Snapper.Snapper import Snapper
from Snapper.AssociationMatrix import AssociationMatrix
from Sensor.Sensor import Sensor
from Relationship.Variable import Variable
from unittest.mock import MagicMock


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
    assert isinstance(manager.route_map[sensor.uuid], Variable)

    manager.remove_sensor(sensor)

    assert manager.sensors == []
    assert manager.variables == []
    assert manager.route_map == {}


def test_add_multiple_sensors():
    manager = Manager()
    sensor1 = Sensor()
    sensor2 = Sensor()
    manager.add_sensor(sensor1)
    manager.add_sensor(sensor2)

    assert manager.sensors == [sensor1, sensor2]
    assert isinstance(manager.variables[0], Variable)
    assert isinstance(manager.variables[1], Variable)
    assert isinstance(manager.route_map[sensor1.uuid], Variable)
    assert isinstance(manager.route_map[sensor2.uuid], Variable)

    manager.remove_sensor(sensor1)
    manager.remove_sensor(sensor2)

    assert manager.sensors == []
    assert manager.variables == []
    assert manager.route_map == {}


def test_return_matrix():
    manager = Manager()
    matrix = manager.get_matrix()

    assert matrix == manager.matrix


def test_push_snapshot():
    manager = Manager()
    sensor1 = Sensor()
    sensor2 = Sensor()
    manager.add_sensor(sensor1)
    manager.add_sensor(sensor2)

    variable1 = manager.route_map[sensor1.uuid]
    variable2 = manager.route_map[sensor2.uuid]

    variable1.on_data = MagicMock()
    variable2.on_data = MagicMock()

    snapshot = {sensor1.uuid: 1, sensor2.uuid: 2}

    manager.on_data(snapshot)

    variable1.on_data.assert_called_with(1)
    variable2.on_data.assert_called_with(2)

def test_get_value_matrix():
    manager = Manager()

    manager.matrix.get_value_matrix = MagicMock()

    manager.get_value_matrix()

    manager.matrix.get_value_matrix.assert_called_with()
