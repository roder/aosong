"""
Copyright 2014 Matt Heitzenroder

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from aosong.am2315 import Sensor
import unittest, time

class TestSensor(unittest.TestCase):

    def setUp(self):
        self.sensor = Sensor()
        self.assertIn(self.sensor.channel, [0,1])
        self.assertIs(self.sensor.address, 0x5c)
        self.assertIsInstance(self.sensor, Sensor)
        self.assertIs(self.sensor.lastError, None)

    def test_pi_revision(self):
        self.assertIn(self.sensor.pi_revision(), [1,2])

    def test_pi_i2c_bus_number(self):
        self.assertIn(self.sensor.pi_i2c_bus_number(), [0,1])

    def test_data(self):
        time.sleep(.5)
        data = self.sensor.data()
        self.assertIsNotNone(data)
        self.assertIs(len(data), 3)

    def test_humidity(self):
        time.sleep(.5)
        self.assertIsNotNone(self.sensor.humidity())

    def test_temperature(self):
        time.sleep(.5)
        self.assertIsNotNone(self.sensor.temperature())
        time.sleep(.5)
        self.assertIsNotNone(self.sensor.temperature(False))
