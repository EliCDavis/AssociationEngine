from AssociationEngine.Sensor.Sensor import Sensor


def test_Sensor_gets_named():
    s = Sensor(name="Name")

    assert str(s) == "Name"


def test_unnamed_Sensor_returns_uuid():
    s = Sensor()

    assert str(s) == str(s.uuid)
