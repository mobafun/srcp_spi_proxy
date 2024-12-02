#!/usr/bin/python
import socket
import sys
import time

from threading import Thread

from srcp_spi_fb.MCP23S17Sensor import MCP23S17Sensor

class RocrailProxy(object):
    def __init__(self,host,port,sensors,srcpbus=10):
        print( "Creating new SRCP proxy @ {}:{}".format(host,port) )
        self.host=host
        self.port=port
        self.srcpbus=srcpbus
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sensors=sensors
        for s in sensors:
            s.open()

        self.sensorThread = None

    def sensing(self,client):
        """ Evaluate sensors in a spearate thread """
        old=0
        time.sleep(1)
        while True:
            val=0
            for chip in (self.sensors):
                val<<=16
                val = val|chip.readSensor()

            diff=old^val

            for i in range(16*len(self.sensors),0,-1):
                if 1<<i-1 & diff:
                    if 1<<i-1 & val:
                        state=1
                    else:
                        state=0
                    msg="{tstamp:d} 100 INFO {bus:d} FB {sensor:d} {val:d}\n".format(tstamp=time.time(), bus=self.srcpbus, sensor=i, val=state)
                    client.sendall(msg)
            old=val
            time.sleep(0.01)



    def request(self,source,sink,connection):
        while True:
            data=source.recv(1024)
            if not data:
                break
            print("[{}] ".format(connection)+str(data.strip()))
            #time.sleep(0.1)
            if data=="SET CONNECTIONMODE SRCP INFO\n":
                source.sendall("202 OK CONNECTIONMODE\n")
                if self.sensorThread is None:
                   self.sensorThread = Thread(target=self.sensing, args=(source,))
                   self.sensorThread.start()
            else:
                sink.sendall(data)

        try:
            source.close()
        except:
            pass

    def response(self, source, sink, connection):
        while True:
            data=source.recv(1024)
            if data:
                sink.sendall(data)
        try:
            source.close()
        except:
            pass


    def forward(self,srcpSock):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host,self.port))
        except OSError as msg:
            print('Bind failed. Error Code : ' + msg.errno + ' Message ' + msg.strerror )
            sys.exit(-3) 
        
        
        self.srcp=srcpSock
        self.socket.listen(10)
        print('Bound to server socket, listening.')
            
        connection=0
                     
        while True:
            client, addr = self.socket.accept()
            print('Incoming connection from {}:{}...'.format(addr[0],addr[1]))
            self.srcp.connect()
            self.requestThread  = Thread(target=self.request, args=(client,self.srcp.socket,connection,))
            self.responseThread = Thread(target=self.response, args=(self.srcp.socket,client,connection,))
            self.requestThread.start()
            self.responseThread.start()
            connection+=1    
 
        self.socket.close()