
from socket import *
from jinja2 import Template
from datetime import datetime
from HttpMessage import HttpMessage
from Network import Network
import urllib.parse
import json
import threading 

server_ip = '127.0.0.1'
port_num = 1024
new_line = "\r\n"

class Server(threading.Thread):

    def __init__(self, messages):
        self.messages = messages
        threading.Thread.__init__(self)
        
        
    #main function
    #sets up a socket then forever recieves a message then returns
    #to exit press the keyboard?
    def run(self):
        try:
            network = Network()
            serversocket = network.serversocket
            try:
                serversocket.listen(5)
            except Exception as e :
                print("Error: " + e)
            while(1): 
                self.HandleRequest(network)
        except KeyboardInterrupt :
            print("\nShutting down...\n")
        finally:
            serversocket.close()

    #input <socket>: a socket that just stopped listening
    def HandleRequest(self,network):
        try:
            (clientsocket, address) = network.serversocket.accept()
        except Exception as e:
            print("socket accept failed" + e)
            return
        httpMessage = HttpMessage(clientsocket)
        httpMessage.Print()
        data = self.HandleMessage(httpMessage, network)
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
    def HandleMessage(self,httpMessage, network):
        #first handle the path 
        #splits the path into its parts
        pathRoutes = httpMessage.pathRoutes
        if pathRoutes[0] in ['','index','favicon.ico']:
            return self.ServeIndex(httpMessage, network)
        #TODO send 403 error message

    #serves a request that is looking for index
    def ServeIndex(self, httpMessage,network):
        if httpMessage.command == 'GET':
            response = self.MakeStatus200()
            response += self.MakeHeader()
            messages, dateTime = self.messages.GetAllMessages()
            response += self.MakeFile("main.html",
                {'messages':zip(dateTime[::-1],messages[::-1]),
                "ipAddress":network.server_ip,
                "portNum": 1025})
            response += new_line
            return response
        '''
        if httpMessage.command == 'POST':
            bodyArray = httpMessage.body.split('=')
            message = bodyArray[1]
            
            words.append(message)
            times.append(str(datetime.now()))
            response = "HTTP/1.1 303 See Other" + new_line
            response += "Location: " + "/index" + new_line
            return response
        '''

    '''
    def ServeMessages(self, httpMessages):
        if httpMessages.command == 'GET':
            response = self.MakeStatus200()
            response += self.MakeHeader()
            #send json in the form [{'time': '12:35', "message":"hello"},{{'time': '1:35', "message":"good bye"}}]
            messagesClientHas = int(httpMessages.urlArgs['numMessages'])

            print(jsonToSend)
            response += json.dumps(jsonToSend)
            return response
        #TODO throw error
    '''


