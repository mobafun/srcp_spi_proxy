
from srcp_spi_fb.MCP23S17 import MCP23S17 


class MCP23S17Sensor(MCP23S17):
    """This class uses MCP23s17 as rail sensor for some of its pins  
    for the Raspberry Pi.
    """

    NUM_QUERIES = 7
    MAJORITY    = 3

    def __init__(self, bus=0, ce=0, deviceID=0x00, mask=0xff):
        """ Constructor
        Initializes only masked pins as sensor input
        Keyword arguments:
        bus The SPI bus number
        
        
        The chip-enable number for the SPI
        deviceID The device ID of the component, i.e., the hardware address (default 0.0)
        mask the GPIO pins to sensor on"""
        super().__init__(bus, ce, deviceID)
        self.mask = mask
        self._resetSensor()

    def open(self):
        """start hardware usage
        Set all pins as input, enable pullout, invert logic.  
        """
        super().open()
        self._writeRegister(MCP23S17.MCP23S17_IPOLA, self.mask & 0xff)
        self._writeRegister(MCP23S17.MCP23S17_IPOLB, self.mask >> 8)
        self._resetSensor()



    def _resetSensor(self):
        self.senseValues = [0 for i in range(16)]
        self.lastState   = 0 
        self.numQueries  = MCP23S17Sensor.NUM_QUERIES


        
    def _internalReadSensor(self):
        val = self.readGPIO() & self.mask
        for offset in range(16):
            if (val & (1<<offset)):
                self.senseValues[offset]+=1 



    def readSensor(self):
        """ Evaluate sensors based on consensur of multiple queries """
        self._internalReadSensor()

        self.numQueries-=1
        if (self.numQueries == 0):
            val = 0 
            for pos in range(16):
                if ( self.senseValues[pos] > MCP23S17Sensor.MAJORITY ):
                    val |= (1 << pos) 
            self._resetSensor() 
            self.lastState = val 

        return self.lastState 
