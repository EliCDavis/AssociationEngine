from Sensor.Sensor import Sensor
from Relationship.Variable import Variable
from Snapper.Snapper import Snapper


def test_should_have_sensors_field_as_empty_list_on_init():
    snapper = Snapper()
    assert len(snapper.sensors) is 0


def test_should_have_variables_field_as_empty_list_on_init():
    snapper = Snapper()
    assert len(snapper.variables) is 0


def test_should_receive_data_from_attached_sensor():
    snapper = Snapper()
    sensor = Sensor(snapper)
    snapper.add_sensor(sensor)
    sensor.publish(2)

    assert snapper.dataBuffer[sensor.uuid] is 2


def test_should_store_sensor():
    snapper = Snapper()
    sensor = Sensor(snapper)
    snapper.add_sensor(sensor)

    assert isinstance(snapper.sensors[0], Sensor)


def test_should_generate_variable():
    snapper = Snapper()
    sensor = Sensor(snapper)
    snapper.add_sensor(sensor)

    assert isinstance(snapper.variables[0], Variable)

