
from socket import *

'''
contains the information for the ip and port
'''
class Network:

    #members of the class
    server_ip = '192.168.1.4'
    port_num = 1024
    
    def __init__(self):
        self.FindPortDynamically()


    #finds a port that is open and returns a binded socket
    #socket used Steam (TCP)
    def FindPortDynamically(self):
        while(True):
            try:
                self.serversocket = socket(AF_INET, SOCK_STREAM)
                self.serversocket.bind((self.server_ip,self.port_num)) # this is the line that fails
                print('Access http://' + self.server_ip + ':' + str(self.port_num))
                return
            except Exception as exc :
                print("Error Finding port " +str(self.port_num) +":\n")
                print(exc)
                self.port_num += 1
    