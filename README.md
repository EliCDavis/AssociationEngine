[![Build Status](https://travis-ci.org/EliCDavis/AssociationEngine.svg?branch=master)](https://travis-ci.org/EliCDavis/AssociationEngine) [![Coverage Status](https://coveralls.io/repos/github/EliCDavis/AssociationEngine/badge.svg?branch=master)](https://coveralls.io/github/EliCDavis/AssociationEngine)

# Association Engine

Engine for generating network maps that displays which sensors are related to others in an IOT setting as a feature for cloud computing.

**Written for Python 3.6 or later**

## Installing

[We doing pip or docker?]

## Developer Setup

```bash
git clone https://github.com/EliCDavis/AssociationEngine
pip install -e .
```

After everythings been installed, try running tests to make sure everythings working correctly

```bash
pytest
```

### Running Example Demo

```bash
cd AssociationEngine/Examples/webpage # After cloning and navigating inside of root
npm install
gulp build
python Server.py
```

If everything goes smoothly you should be able to open up localhost:5000 in your favorite web browser