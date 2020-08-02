
from socket import AF_INET, socket, SOCK_STREAM

'''
contains the information for the ip and port
'''
class Network:

    #members of the class
    ServerIp = '192.168.1.4'
    
    ServerPortNum = 1024

    
    def __init__(self):
        self.WebsocketPortNum = 0
        self.FindHttpServerPortDynamically()
        pass


    #opens a socket on an open port for the http server
    def FindHttpServerPortDynamically(self):
        while(True):
            try:
                self.serversocket = socket(AF_INET, SOCK_STREAM)
                self.serversocket.bind((self.ServerIp,self.ServerPortNum)) # this is the line that fails
                self.WebsocketPortNum = self.ServerPortNum + 1
                print('Access http://' + self.ServerIp + ':' + str(self.ServerPortNum))
                return
            except Exception as exc :
                print("Error Finding port " +str(self.ServerPortNum) +":\n")
                print(exc)
                self.ServerPortNum += 1