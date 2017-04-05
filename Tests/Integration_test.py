from Snapper.Manager import Manager
from Sensor.Sine import Sine
from Sensor.Cosine import Cosine


def test_integration():

    sensors = [Sine(), Cosine()]

    # Setup Engine
    ae = Manager()
    ae.add_sensor(sensors[0])
    ae.add_sensor(sensors[1])

    # Simulate a user's Program Loop
    for time in range(36):
        for sensor in sensors:
            sensor.tick(time/10.0)

    # It didn't break
    assert True
