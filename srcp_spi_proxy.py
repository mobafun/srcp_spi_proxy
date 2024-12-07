#!/usr/bin/python

import sys
import argparse

from srcp_spi_fb import SRCPSock, RocrailProxy, MCP23S17Sensor  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='srcp_spi_proxy',
                    description='Loop in SPI feedback into srcpd communication with rocrail')
    
    parser.add_argument('--bus', type=int, default=0, help='SPI bus')
    parser.add_argument('--ce', type=int, default=0, help='Clock enable pin')
    parser.add_argument('--dev', type=int, default=0, help='SPI device id')
    parser.add_argument('reqport', type=int, help='Rocrail request port (4304)')
    parser.add_argument('srcpdport', type=int, help='Srcpd daemon port (4303)')
    args = parser.parse_args(sys.argv)

    sensor1 = MCP23S17Sensor(bus=args['bus'], ce=args['ce'],
                deviceID=args['dev'])
    
    # move srcp to the non-standard port
    srcpSock = SRCPSock('localhost', args['reqport'])
    srcpSock.connect()

    # make proxy available on srcp standard port
    proxy = RocrailProxy('localhost', args['srcpdport'], sensors=[ sensor1 ])
    proxy.forward(srcpSock)
