[![Build Status](https://travis-ci.org/EliCDavis/AssociationEngine.svg?branch=master)](https://travis-ci.org/EliCDavis/AssociationEngine) [![Coverage Status](https://coveralls.io/repos/github/EliCDavis/AssociationEngine/badge.svg?branch=master)](https://coveralls.io/github/EliCDavis/AssociationEngine)

# Association Engine

The main objective of the project is to establish a means of automatically detecting and reporting associations between streams of data from a wide assortment of sensors. Our system will monitor the sensor data constantly in the background, maintaining an assessment of the relationships between each pair of sensors.

**Written for Python 3.6 or later**

## Running Example Server in Docker

This example comes with a compressed version of NOAA weather data for Birmingham (AL), Columbus (MS), Biloxi (MS), and Las Vegas (NV). The Docker image will immediately launch a server on 5000 which runs the Association Engine on a sped-up simulation of the data.
```bash
docker run -p 5000:5000 -it jacobamason/association-engine
```

## Installing
To get Association Engine as a Python package:
```bash
pip install association-engine
```

You can then `import AssociationEngine` and use `AssociationEngine.Manager` and `AssociationEngine.Sensor` for whatever you need.

### Example
```python
import AssociationEngine

class MyCustomSensor(AssociationEngine.Sensor):

    def some_function(self):
        self.publish(some_data, some_time)


class MySubscriber:

    def on_data(self, value):
        print("The association value is: " + str(value)):


AE = AssociationEngine.Manager()
sensor_one = MyCustomSensor()
sensor_two = MyCustomSensor()

AE.add_sensor(sensor_one)
AE.add_sensor(sensor_two)

relationship = AE.get_relationship_from_sensors(sensor_one, sensor_two)
relationship.subscribe(MySubscriber())
```

## Developer Setup

```bash
git clone https://github.com/EliCDavis/AssociationEngine
pip install -e .
```

After everything has been installed, try running tests to make sure everything is working correctly

```bash
pytest
```
