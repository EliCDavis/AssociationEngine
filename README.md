[![Build Status](https://travis-ci.org/EliCDavis/AssociationEngine.svg?branch=master)](https://travis-ci.org/EliCDavis/AssociationEngine) [![Coverage Status](https://coveralls.io/repos/github/EliCDavis/AssociationEngine/badge.svg?branch=master)](https://coveralls.io/github/EliCDavis/AssociationEngine)

# Association Engine

Engine for generating network maps that displays which sensors are related to others in an IOT setting as a feature for cloud computing.

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

## Developer Setup

```bash
git clone https://github.com/EliCDavis/AssociationEngine
pip install -e .
```

After everything has been installed, try running tests to make sure everything is working correctly

```bash
pytest
```
