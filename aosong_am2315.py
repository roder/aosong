"""---------------------------------------------------------------------------
aosong_am2315.py

Written by Sopwith
03 May 2014

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
 Python application that wraps the capabilities of the AOSONG AM2315 humidity
 and temperature sensor.
 The datasheet for the device can be found here:
 http://www.adafruit.com/datasheets/AM2315.pdf
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
 NOTE: Portions of this code were inspired by Joehrg Ehrsam's am2315-python-api
       code. http://code.google.com/p/am2315-python-api/
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
 Revision history:
 	 2014-09-16 - Fixed negative temperature masking error
     2014-05-01 - Initial release
#--------------------------------------------------------------------------"""
import quick2wire.i2c as i2c
import time
import array
import math

def main():

    sensor = AOSONG_AM2315()

    print('Pi version = ', sensor.pi_rev)
    print('Sensor is on channel ', sensor.channel, sep='')

    print()
    print('ReadSensorData() = ', sensor.ReadSensorData(), sep='')
    data = sensor.ReadSensorData()
    print('Humidity = ', data[0], '%', sep='')
    print('Temperature = ', data[1], 'C', sep='')
    print('Temperature = ', data[2], 'F', sep='')

    print()

    print('ReadHumidity() = ', sensor.ReadHumidity())
    print('lastError: ', sensor.lastError)
    print('ReadTemperature() = ', sensor.ReadTemperature())
    # Pass True to ReadTemperature() to read temp in degrees Fahrenheit
    print('ReadTemperature(True) = ', sensor.ReadTemperature(True))
    print('lastError: ', sensor.lastError)
    
class AOSONG_AM2315:
    """Wrapping for an AOSONG AM2315 humidity and temperature sensor.

    Provides simple access to a AM2315 chip using the quickwire i2c module
    Attributes:
        channel:   Int containing the smbus channel.
        address:   AM2315 bus address
        pi_rev:    Int containing Pi board revision.
        bus:       quickwire i2c object instance.
        lastError: String containing the last error string.Formatter
        debug:     bool containing debug state
    """
    def __init__(self, address=0x5C, debug=False):
        self.version = 1.0
        self.channel = self.GetPiI2CBusNumber()   # 0 for pi Rev-1, 1 for pi Rev-2
        self.address = address   				  # Default address 0x5C
        self.pi_rev = self.GetPiRevision()		  # Pi board revision number  
        self.bus = i2c.I2CMaster() 				  # quick2wire master
        self.lastError = None   				  # Contains last error string

        self.debug = debug       				  # Debug flag

    def GetPiRevision(self):
        """Get the version number of the Raspberry Pi board.
    
        Args:
            None
        Returns:

            An int containing the Pi board revision (1 or 2).
            If error, returns 0.
        """
        return i2c.revision()

    def GetPiI2CBusNumber(self):
        """Get the I2C bus number /dev/i2c.
       
        Args:
            None
        Returns:
            An int containing i2c bus number
        """
        if i2c.revision() > 1:
            return 1
        else:
            return 0

    def ReadSensorData(self):
        """ Reads the humidity and temperature from the AS2315.

        Args:
            None
        Returns:
            Tuple containing the following fields:
                humidity    - float


                temperature - float (Celsius)
                temperature - float (Fahrenheit)
        """
        data = None

        # Send a wakeup call to the sensor. This call will always fail
        try:
            self.bus.transaction(i2c.writing(self.address, bytes([0x03,0x0,0x04])))
        except:
             pass

        time.sleep(0.125)
        # Now that the device is awake, read the data
        try:
            self.bus.transaction(i2c.writing(self.address, bytes([0x03,0x0,0x04])))
            data = self.bus.transaction(i2c.reading(self.address, 0x08))
            data = bytearray(data[0])
        except IOError as e:
            self.lastError = 'I/O Error({0}): {1}'.format(e.errno,e.strerror)
            return None

        # 0x03-returned command, 0x04-no bytes read.
        if data[0] != 0x03 and data[1] != 0x04:
            self.lastError('Error reading data from AM2315 device.')
            return None
    
        # Parse the data list
        cmd_code = data[0]
        byte_cnt = data[1]
        humid_H  = data[2]
        humid_L  = data[3]
        temp_H   = data[4]
        temp_L   = data[5]
        crc_H    = data[6]
        crc_L    = data[7]

        negative = False
        humidity = (humid_H*256+humid_L)/10

        # Check for negative temp
		# 16-Sep-2014
		# Thanks to Ethan for pointing out this bug!
		# ethansimpson@xtra.co.nz
        if temp_H&0x08:
           negative = True
        # Mask the negative flag
        temp_H &=0x7F

        tempC = (temp_H*256+temp_L)/10
        tempF = self.CelsiusToFahrenheit(tempC)

        # Verify CRC here

        crc = 256*data[7] + data[6]
        t = bytearray([data[0], data[1], data[2], data[3], data[4], data[5]])
        c = self.VerifyCRC(t)

        if crc != c:
            assert(0)
            self.lastError('CRC error in sensor data.')
            return None
        
        if negative:
            tempC = -abs(tempC)
            tempF = -abs(tempF)

        return (humidity, tempC, tempF)


    def ReadHumidity(self):
        """Read humidity data from the sensor.

        Args:
            None
        Returns:
            float = humidity reading, None if error
        """
        time.sleep(.25)
        data = self.ReadSensorData()
        if data != None:
            return self.ReadSensorData()[0]
        return None

    def ReadTemperature(self, fahrenheit=False):
        """Read temperature data from the sensor. (Celsius is default)

        Args:
            bool - if True returns temp in Fahrenheit. Default=False
        Returns:
            float = humidity reading, None if error
        """
        time.sleep(.25)
        data = self.ReadSensorData()
        if data == None:
            return None
        if fahrenheit:
            return self.ReadSensorData()[2]
        return self.ReadSensorData()[1]


    def VerifyCRC(self, char):
        """Returns the 16-bit CRC of sensor data"""
        crc = 0xFFFF
        for l in char:
            crc = crc ^ l
            for i in range(1,9):
                if(crc & 0x01):
                    crc = crc >> 1
                    crc = crc ^ 0xA001
                else:
                    crc = crc >> 1
        return crc


    def CelsiusToFahrenheit(self, celsius):
        """Convert Celsius to Fahrenheit.

        Params:
            celsius: int containing C temperature

        Returns:
            String with Fahrenheit conversion. None if error.
        """
        if celsius == None:
           return

        if celsius == 0:
            return 32

        try:
            tempF = float((celsius*9/5)+32)
            return (math.trunc(tempF*10))/10
        except:

            self.lastError = 'Error converting %s celsius to fahrenheit' % celsius
            return None

    
    def GetLastError(self):
        return self.lastError
    
if __name__ == "__main__":
    main()
    
