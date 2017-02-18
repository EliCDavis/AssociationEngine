from ..Sensor.Sensor import Sensor
from .Snapper import Snapper


def test_should_have_sensors_field_as_empty_list_on_init():
    snapper = Snapper()
    assert len(snapper.sensors) is 0


def test_should_have_variables_field_as_empty_list_on_init():
    snapper = Snapper()
    assert len(snapper.variables) is 0


def test_should_receive_data_from_attached_sensor():
    snapper = Snapper()
    sensor = Sensor(snapper)
    snapper.sensors.append(sensor)  # A little hacked, I know. This is a place-holder
    sensor.Publish(2)

    assert snapper.dataBuffer[sensor.uuid] is 2