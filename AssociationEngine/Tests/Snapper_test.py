from unittest.mock import MagicMock

from AssociationEngine.Snapper.Manager import Manager
from AssociationEngine.Snapper.Snapper import Snapper

from AssociationEngine.Sensor.Sensor import Sensor


def test_should_have_sensors_field_as_empty_list_on_init():
    snapper = Snapper()
    assert snapper.sensors == []


def test_should_change_window_size():
    snapper = Snapper()

    snapper.set_window_size(20)

    assert snapper.timeWindow == 20

    snapper.set_window_size(5.00)

    assert round(snapper.timeWindow - 5.00, 5) == 0.0


def test_should_receive_data_from_attached_sensor():
    snapper = Snapper()
    sensor = Sensor()
    snapper.add_sensor(sensor)
    sensor.publish(2)

    assert snapper.dataBuffer[sensor.uuid] == [2]


def test_should_receive_data_from_multiple_sensors():
    snapper = Snapper()
    sensor1 = Sensor()
    snapper.add_sensor(sensor1)
    sensor1.publish(2)
    sensor2 = Sensor()
    snapper.add_sensor(sensor2)
    sensor2.publish(3)

    assert snapper.dataBuffer == {sensor1.uuid: [2], sensor2.uuid: [3]}
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
    sensor1.publish(2, 1)
    sensor2 = Sensor()
    snapper.add_sensor(sensor2)
    sensor2.publish(3, 1)
    # Force a snapshot publish by pushing value with time past window
    sensor2.publish(3, 11)

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

    assert round(snapshot[sensor_a.uuid] - 1, 5) == 0
    assert round(snapshot[sensor_b.uuid] - 3, 5) == 0


def test_should_use_none_for_sensors_not_pushing():
    snapper = Snapper()
    sensor_a = Sensor()
    snapper.add_sensor(sensor_a)
    sensor_b = Sensor()
    snapper.add_sensor(sensor_b)
    sensor_b.publish(3)

    snapshot = snapper.get_snapshot()

    assert sensor_a.uuid in snapshot

    assert snapshot[sensor_a.uuid] is None
    assert round(snapshot[sensor_b.uuid] - 3, 5) == 0


def test_aggregation_averaging():
    snapper = Snapper()
    sensor_a = Sensor()
    snapper.add_sensor(sensor_a)
    sensor_b = Sensor()
    snapper.add_sensor(sensor_b)

    sensor_a.publish(1, 1)
    sensor_a.publish(5, 2)
    sensor_a.publish(6, 2)
    sensor_a.publish(4, 2)

    sensor_b.publish(3, 2)
    sensor_b.publish(7, 2)
    sensor_b.publish(2, 2)
    sensor_b.publish(4, 2)
    sensor_b.publish(5, 2)
    sensor_b.publish(2, 2)
    sensor_b.publish(6, 2)
    sensor_b.publish(9, 2)

    snapshot = snapper.get_snapshot()

    assert round(snapshot[sensor_a.uuid] - 4, 5) == 0
    assert round(snapshot[sensor_b.uuid] - 4.75, 5) == 0


def test_should_generate_and_return_multiple_snapshots_correctly():
    snapper = Snapper()
    sensor_a = Sensor()
    snapper.add_sensor(sensor_a)
    sensor_a.publish(1, 1)
    sensor_a.publish(5, 6)
    sensor_b = Sensor()
    snapper.add_sensor(sensor_b)
    sensor_b.publish(3, 7)
    sensor_b.publish(9, 8)

    snapshot1 = snapper.get_snapshot()

    assert round(snapshot1[sensor_a.uuid] - 3, 5) == 0
    assert round(snapshot1[sensor_b.uuid] - 6, 5) == 0

    sensor_a.publish(5, 11)
    sensor_a.publish(10, 12)
    sensor_a.publish(15, 13)
    sensor_b.publish(6, 13)
    sensor_b.publish(12, 14)
    sensor_b.publish(2, 15)
    sensor_b.publish(30, 16)

    snapshot2 = snapper.get_snapshot()

    assert round(snapshot2[sensor_a.uuid] - 10, 5) == 0
    assert round(snapshot2[sensor_b.uuid] - 12.5, 5) == 0


def test_should_use_changed_time_window_for_snapshot_after_change():
    manager = Manager()
    manager.on_data = MagicMock()
    snapper = Snapper(manager)
    sensor1 = Sensor()
    snapper.add_sensor(sensor1)
    sensor1.publish(2, 1)

    # Change window size in middle of data transmission
    snapper.set_window_size(15.0)

    sensor2 = Sensor()
    snapper.add_sensor(sensor2)
    sensor2.publish(3, 1)
    # Force a snapshot publish by pushing value with time past original window
    sensor2.publish(3, 11)

    # Should finish original window and push the resulting snapshot before transitioning
    manager.on_data.assert_called_with({sensor1.uuid: 2, sensor2.uuid: 3})

    # Push values within the new window
    sensor1.publish(3, 15)
    sensor2.publish(5, 16)

    # Force a snapshot push by publishing out of bounds data
    sensor1.publish(3, 26)

    manager.on_data.assert_called_with({sensor1.uuid: 3, sensor2.uuid: 4})
