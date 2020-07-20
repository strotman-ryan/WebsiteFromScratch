'''
The entry point into running the server
Starts two threads
    1. http thread that will handle normal HTTP requests
    2. web socket thread that will handle websockets
Creates a shared object
    1. messeging object
        - stored messges and their times 
        - thread safe getters and setters
'''

from Server import Server
from WebSocketServer import WebSocketServer
from Messages import Messages

def main():
    messages = Messages()
    httpThread = Server(messages)
    ipAddress = httpThread.network.server_ip
    portNum = httpThread.network.port_num + 1
    webSocketThread = WebSocketServer(messages, ipAddress, portNum)

    webSocketThread.start()
    httpThread.start()
    


if __name__ == "__main__":
    main()