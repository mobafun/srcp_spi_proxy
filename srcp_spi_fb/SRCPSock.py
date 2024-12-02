import socket
import sys
import time

class SRCPSock(object):

    def close(self):
        self.socket.close()
        print("Disconnected from SRCP!")
    
    def __init__(self, host, port):
        self.port=port
        try:
            self.host=socket.gethostbyname(host)
        except:
            print("Hostname "+ self.host +" could not be resolved. Exiting")
            sys.exit(-2)            
        

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print("Client socket created.")
        except OSError as msg:
            print("Failed to create socket. Error code: "+ msg.errno +", Error message: "+ msg.strerror)
            sys.exit(-1)

        self.socket.connect((self.host , self.port))
        print( "SRCP connected @ {}:{}".format(self.port,self.host) )
        