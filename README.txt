#-----------------------------------------------------------------------------#
aosong_am2315.py
Written by Sopwith
3 May 2014
#-----------------------------------------------------------------------------#
Python3 wrapper class for AOSONG AM2315 temperature/humidity sensor. The code
is clean and well commented.
NOTE: This code only works on Python3.
      It requires the quick2wire python api library.
      https://github.com/quick2wire/quick2wire-python-api

Sample useage:
--------------
$ python3
Python 3.2.3 (default, Mar  1 2013, 11:53:50) 
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from aosong_am2315 import AOSONG_AM2315
>>> sensor = AOSONG_AM2315()
>>> print(sensor.ReadSensorData())
(41.8, 23.5, 74.3)
>>> print(sensor.ReadHumidity())
41.8
>>> print(sensor.ReadTemperature())
23.5
>>> print(sensor.ReadTemperature(True))
74.4
>>> 

Default script behavior:
------------------------
Running the aosong_am2315.py script shows the capabilities of the class.
$ python3 aosong_am2315.py 
Pi version =  2
Sensor is on channel 1

ReadSensorData() = (40.8, 23.8, 74.8)
Humidity = 40.8%
Temperature = 23.8C
Temperature = 74.8F

ReadHumidity() =  40.8
lastError:  None
ReadTemperature() =  23.8
ReadTemperature(True) =  74.8
lastError:  None

Test script:
------------
test_aosong_am2315.py is a unittest script you should run to ensure your sensor
is wired correctly. If it is, you should see the below test results.

$ python3 test_aosong_am2315.py 
.....
----------------------------------------------------------------------
Ran 5 tests in 3.705s

OK
 
Notes
-----
ReadSensorData() returns a tuple containing three values.
    (41.8, 23.5, 74.3)
    The first value is the current relative humidity
    The second value is the current temperature in Celsius.
    The third value is the current temperature in Fahrenheit.

ReadTemperature() returns the current temperature in Celsius.
    If you want the current temperature returned in Fahrenheit
    pass True as a parameter.
    ReadTemperature(True)

Please send bugs, comments, enhancement requests to:
sopwith@ismellsmoke.net
http://sopwith.ismellsmoke.net




 



