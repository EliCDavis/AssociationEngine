from Sensor.Sensor import Sensor
from Snapper.Snapper import Snapper
from Snapper.Manager import Manager
from unittest.mock import MagicMock


def test_should_have_sensors_field_as_empty_list_on_init():
    snapper = Snapper()
    assert snapper.sensors == []


def test_should_receive_data_from_attached_sensor():
    snapper = Snapper()
    sensor = Sensor()
    snapper.add_sensor(sensor)
    sensor.publish(2)

    assert snapper.dataBuffer[sensor.uuid] is 2


def test_should_receive_data_from_multiple_sensors():
    snapper = Snapper()
    sensor1 = Sensor()
    snapper.add_sensor(sensor1)
    sensor1.publish(2)
    sensor2 = Sensor()
    snapper.add_sensor(sensor2)
    sensor2.publish(3)

    assert snapper.dataBuffer == {sensor1.uuid: 2, sensor2.uuid: 3}
    assert snapper.get_snapshot() == {sensor1.uuid: 2, sensor2.uuid: 3}


def test_should_properly_generate_snapshot_from_complete_data():
    snapper = Snapper()
    sensor1 = Sensor()
    snapper.add_sensor(sensor1)
    sensor2 = Sensor()
    snapper.add_sensor(sensor2)

    sensor1.publish(2)

    assert snapper.snapshot == {}

    sensor2.publish(3)

    assert snapper.get_snapshot() == {sensor1.uuid: 2, sensor2.uuid: 3}


def test_should_forward_snapshot_once_data_complete():
    manager = Manager()
    manager.on_data = MagicMock()
    snapper = Snapper(manager)
    sensor1 = Sensor()
    snapper.add_sensor(sensor1)
    sensor1.publish(2)
    sensor2 = Sensor()
    snapper.add_sensor(sensor2)
    sensor2.publish(3)

    manager.on_data.assert_called_with({sensor1.uuid: 2, sensor2.uuid: 3})


def test_should_store_sensor():
    snapper = Snapper()
    sensor = Sensor()
    snapper.add_sensor(sensor)

    assert snapper.sensors == [sensor]


def test_should_remove_sensor():
    snapper = Snapper()
    sensor = Sensor()
    snapper.add_sensor(sensor)
    snapper.remove_sensor(sensor)

    assert snapper.sensors == []


def test_should_generate_and_return_snapshot():
    snapper = Snapper()
    sensor_a = Sensor()
    snapper.add_sensor(sensor_a)
    sensor_a.publish(1)
    sensor_b = Sensor()
    snapper.add_sensor(sensor_b)
    sensor_b.publish(3)

    snapshot = snapper.get_snapshot()

    assert snapshot[sensor_a.uuid] is 1
    assert snapshot[sensor_b.uuid] is 3
