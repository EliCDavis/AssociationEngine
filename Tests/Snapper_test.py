from Sensor.Sensor import Sensor
from Snapper.Snapper import Snapper


def test_should_have_sensors_field_as_empty_list_on_init():
    snapper = Snapper()
    assert snapper.sensors == []


def test_should_receive_data_from_attached_sensor():
    snapper = Snapper()
    sensor = Sensor()
    snapper.add_sensor(sensor)
    sensor.publish(2)

    assert snapper.dataBuffer[sensor.uuid] is 2


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
