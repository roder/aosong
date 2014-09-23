"""
Python wrapper exposes the capabilities of the AOSONG AM2315 humidity
and temperature sensor.
The datasheet for the device can be found here:
http://www.adafruit.com/datasheets/AM2315.pdf

Portions of this code were inspired by Joehrg Ehrsam's am2315-python-api
code. http://code.google.com/p/am2315-python-api/

This library was originally authored by Sopwith:
    http://sopwith.ismellsmoke.net/?p=104

"""
import quick2wire.i2c as i2c
import time
import array
import math

class Sensor:
    """Wrapping for an AOSONG AM2315 humidity and temperature sensor.

    Provides simple access to a AM2315 chip using the quickwire i2c module
    Attributes:
        channel:   Int containing the smbus channel.
        address:   AM2315 bus address
        bus:       quickwire i2c object instance.
        lastError: String containing the last error string.Formatter
        debug:     bool containing debug state
    """
    def __init__(self, address=0x5C, debug=False):
        self.channel = self.pi_i2c_bus_number()   # 0 for pi Rev-1, 1 for pi Rev-2
        self.address = address   				  # Default address 0x5C
        self.bus = i2c.I2CMaster() 				  # quick2wire master
        self.lastError = None   				  # Contains last error string

        self.debug = debug       				  # Debug flag

    def pi_revision(self):
        """Get the version number of the Raspberry Pi board.
    
        Args:
            None
        Returns:

            An int containing the Pi board revision (1 or 2).
            If error, returns 0.
        """
        return i2c.revision()

    def pi_i2c_bus_number(self):
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

    def data(self):
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
        tempF = self.c_to_f(tempC)

        # Verify CRC here

        crc = 256*data[7] + data[6]
        t = bytearray([data[0], data[1], data[2], data[3], data[4], data[5]])
        c = self.verify_crc(t)

        if crc != c:
            assert(0)
            self.lastError('CRC error in sensor data.')
            return None
        
        if negative:
            tempC = -abs(tempC)
            tempF = -abs(tempF)

        return (humidity, tempC, tempF)


    def humidity(self):
        """Read humidity data from the sensor.

        Args:
            None
        Returns:
            float = humidity reading, None if error
        """
        time.sleep(.25)
        data = self.data()
        if data != None:
            return self.data()[0]
        return None

    def temperature(self, fahrenheit=False):
        """Read temperature data from the sensor. (Celsius is default)

        Args:
            bool - if True returns temp in Fahrenheit. Default=False
        Returns:
            float = humidity reading, None if error
        """
        time.sleep(.25)
        data = self.data()
        if data == None:
            return None
        if fahrenheit:
            return self.data()[2]
        return self.data()[1]

    def fahrenheit(self):
        return self.temperature(True)

    def celsius(self):
        return self.temperature()

    def verify_crc(self, char):
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


    def c_to_f(self, celsius):
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

    
    def last_error(self):
        return self.lastError
    
