
from socket import SHUT_WR
from jinja2 import Template
from datetime import datetime
from HttpMessage import HttpMessage
from Network import Network
import urllib.parse
import json
import threading 

new_line = "\r\n"

class HttpServer(threading.Thread):

    def __init__(self, messages, network):
        self.messages = messages
        threading.Thread.__init__(self)
        self.network = network

        
        
    #main function
    #sets up a socket then forever recieves a message then returns
    #to exit press the keyboard?
    def run(self):
        try:
            try:
                self.network.serversocket.listen(5)
            except Exception as e :
                print("Error: " + e)
            while(1): 
                self.HandleRequest()
        except KeyboardInterrupt :
            print("\nShutting down...\n")
        finally:
            self.network.serversocket.close()

    #input <socket>: a socket that just stopped listening
    def HandleRequest(self):
        try:
            (clientsocket, address) = self.network.serversocket.accept()
        except Exception as e:
            print("socket accept failed" + e)
            return
        httpMessage = HttpMessage(clientsocket)
        httpMessage.Print()
        data = self.HandleMessage(httpMessage)
        clientsocket.sendall(data.encode())
        clientsocket.shutdown(SHUT_WR)


    def MakeStatus200(self):
        return "HTTP/1.1 200 OK" + new_line 

    def MakeHeader(self):
        header = "Content-Type: text/html; charset=utf-8" + new_line
        header += new_line 
        return header

    def MakeFile(self,filePath, counter):
        file = open(filePath, "r")
        content = file.read()
        file.close()
        temp = Template(content)
        return temp.render(counter)

    #parses the httpMessage and makes a response
    #input <httpMessage> = type HttpMssage and contains all the request information
    #output <string> = the http response to send back
    def HandleMessage(self,httpMessage):
        #first handle the path 
        #splits the path into its parts
        pathRoutes = httpMessage.pathRoutes
        if pathRoutes[0] in ['','index','favicon.ico']:
            return self.ServeIndex(httpMessage)
        #TODO send 403 error message

    #serves a request that is looking for index
    def ServeIndex(self, httpMessage):
        if httpMessage.command == 'GET':
            response = self.MakeStatus200()
            response += self.MakeHeader()
            messages, dateTime = self.messages.GetAllMessages()
            response += self.MakeFile("Views/main.html",
                {'messages':zip(dateTime[::-1],messages[::-1]),
                "ipAddress":self.network.ServerIp,
                "portNum": self.network.WebsocketPortNum}) #port address for sebsocket server
            response += new_line
            return response


