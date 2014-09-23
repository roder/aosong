"""---------------------------------------------------------------------------
test_aosong_am2315.py

Written by Sopwith
04 May 2014

Redistribution and use in source and binary forms, with or without
modification, are permitted. Use of this software for illegal or
malicious purposed is strictly prohibited. Attribution to the creator(s)
is appreciated but not required.

THIS SOFTWARE IS PROVIDED BY THE CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-----------------------------------------------------------------------------
 Python test application for the aosong_am2315.py script
#-----------------------------------------------------------------------------
 Revision history:
	2014-05-04 - Initial release

#--------------------------------------------------------------------------"""
from aosong_am2315 import AOSONG_AM2315
import unittest, time

class TestAOSONG_AM2315(unittest.TestCase):

    def setUp(self):
        self.sensor = AOSONG_AM2315()
        self.assertIn(self.sensor.channel, [0,1])
        self.assertIs(self.sensor.address, 0x5c)
        self.assertIn(self.sensor.pi_rev, [1,2])
        self.assertIsInstance(self.sensor, AOSONG_AM2315)
        self.assertIs(self.sensor.lastError, None)
            
    def test_GetPiRevision(self):
        self.assertIn(self.sensor.GetPiRevision(), [1,2])
        
    def test_GetPiI2CBusNumber(self):
        self.assertIn(self.sensor.GetPiI2CBusNumber(), [0,1])

    def test_ReadSensorData(self):
        time.sleep(.5)
        data = self.sensor.ReadSensorData()
        self.assertIsNotNone(data)
        self.assertIs(len(data), 3)

    def test_ReadHumidity(self):
        time.sleep(.5)
        self.assertIsNotNone(self.sensor.ReadHumidity())

    def test_ReadTemperature(self):
        time.sleep(.5)
        self.assertIsNotNone(self.sensor.ReadTemperature())
        time.sleep(.5)
        self.assertIsNotNone(self.sensor.ReadTemperature(False))

if __name__ == '__main__':
    unittest.main()
    
