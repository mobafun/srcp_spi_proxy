#!/usr/bin/python

import socket
import sys
import time

from srcp_spi_fb import SRCPSock, RocrailProxy, MCP23S17Sensor  

if __name__ == "__main__":
    sensor1 = MCP23S17Sensor(bus=0x0a,ce=0x00,
                deviceID=0x00,mask=0b0000000000111111)
    
    # move srcp to the non-standard port
    srcpSock = SRCPSock('localhost', 4304)
    srcpSock.connect()

    # make proxy available on srcp standard port
    proxy = RocrailProxy('localhost', 4303, sensors=[ sensor1 ])
    proxy.forward(srcpSock)
