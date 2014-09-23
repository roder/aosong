# AOSONG Sensors

Python package that provides support for AOSONG Sensor.

This package and it's modules have been organized to support additional AOSONG
sensors. It currently only supports the [AM2315 Temperature and Humidity
Sensor](https://www.adafruit.com/datasheets/AM2315.pdf). Additional sensors are
encouraged and welcomed.  Please submit a Pull Request.

The original author of this library was
[Sopwith](http://sopwith.ismellsmoke.net). This repository was originally forked
from the code provided by the author on [their
blog](http://sopwith.ismellsmoke.net/?p=104).  The purpose of the repository is
to provide a pythonic library that can be installed with `pip` and `setuptools`.

## Requirements

* Python 3
* [Quick2wire Python API](https://github.com/quick2wire/quick2wire-python-api)

## Installation

### Recommended
```shell
pip install -e git+https://github.com/roder/aosong@0.0.1
```

### Manual
`python setup.py install`

## Usage

```python
>>> from aosong import am2315
>>> sensor = am2315.Sensor()
>>> sensor.temperature()
19.1
>>> sensor.celsius()
19.1
>>> sensor.fahrenheit()
66.3
>>> sensor.temperature(True)
66.3
>>> sensor.humidity()
70.1
>>> sensor.data()
(70.0, 19.1, 66.3)
>>>

```

### Sensor.data()
Sensor.data() returns a tuple containing three values.

`(41.8, 23.5, 74.3)`

The first value is the current relative humidity
The second value is the current temperature in Celsius.
The third value is the current temperature in Fahrenheit.

### Sensor.temperature()

Sensor.temperature() returns the current temperature in Celsius.

If you want the current temperature returned in Fahrenheit pass True as a parameter.
    
`sensor.temperature(True)`

## Test script:

am2315.py is a unittest script you should run to ensure your sensor
is wired correctly. If it is, you should see the below test results.

`python setup.py test`

## Support and Contribution

Pull requests and Issues are welcome!

Otherwise, please feel free to report bugs, comments, enhancement requests to:
[sopwith@ismellsmoke.net](mailto:sopwith@ismellsmoke.net)
[http://sopwith.ismellsmoke.net](http://sopwith.ismellsmoke.net)

