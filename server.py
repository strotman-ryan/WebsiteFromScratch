
from socket import *
from jinja2 import Template
from datetime import datetime
from HttpMessage import HttpMessage
from Network import Network
import urllib.parse
import json

server_ip = '192.168.1.4'
port_num = 80
new_line = "\r\n"

words = []
times = []
counter = 0


#main function
#sets up a socket then forever recieves a message then returns
#to exit press the keyboard?
def main():
    try:
        network = Network()
        serversocket = network.serversocket
        try:
            serversocket.listen(5)
        except Exception as e :
            print("Error: " + e)
        while(1): 
            HandleRequest(network)
    except KeyboardInterrupt :
        print("\nShutting down...\n")
    finally:
        serversocket.close()

#input <socket>: a socket that just stopped listening
def HandleRequest(network):
    try:
        (clientsocket, address) = network.serversocket.accept()
    except Exception as e:
        print("socket accept failed" + e)
        return
    httpMessage = HttpMessage(clientsocket)
    httpMessage.Print()
    data = HandleMessage(httpMessage, network)
    clientsocket.sendall(data.encode())
    clientsocket.shutdown(SHUT_WR)


def MakeStatus200():
    return "HTTP/1.1 200 OK" + new_line 

def MakeHeader():
    header = "Content-Type: text/html; charset=utf-8" + new_line
    header += new_line 
    return header

def MakeFile(filePath, counter):
    file = open(filePath, "r")
    content = file.read()
    file.close()
    temp = Template(content)
    return temp.render(counter)

#parses the httpMessage and makes a response
#input <httpMessage> = type HttpMssage and contains all the request information
#output <string> = the http response to send back
def HandleMessage(httpMessage, network):
    #first handle the path 
    #splits the path into its parts
    pathRoutes = httpMessage.pathRoutes
    if pathRoutes[0] in ['','index','favicon.ico']:
        return ServeIndex(httpMessage, network)
    if pathRoutes[0] in ['messages']:
        return ServeMessages(httpMessage)
    #TODO send 403 error message

#serves a request that is looking for index
def ServeIndex(httpMessage,network):
    if httpMessage.command == 'GET':
        response = MakeStatus200()
        response += MakeHeader()
        response += MakeFile("main.html",
            {'counter':counter,
            'messages':zip(times[::-1],words[::-1]),
            "ipAddress":network.server_ip,
            "portNum": network.port_num})
        response += new_line
        return response
    if httpMessage.command == 'POST':
        bodyArray = httpMessage.body.split('=')
        message = bodyArray[1]
        message = urllib.parse.unquote_plus(message)
        words.append(message)
        times.append(str(datetime.now()))
        response = "HTTP/1.1 303 See Other" + new_line
        response += "Location: " + "/index" + new_line
        return response


def ServeMessages(httpMessages):
    if httpMessages.command == 'GET':
        response = MakeStatus200()
        response += MakeHeader()
        #send json in the form [{'time': '12:35', "message":"hello"},{{'time': '1:35', "message":"good bye"}}]
        messagesClientHas = int(httpMessages.urlArgs['numMessages'])
        jsonToSend = []
        for time, content in zip(times[messagesClientHas::], words[messagesClientHas::]):
            message = {}
            message["time"] = time
            message["message"] = content
            jsonToSend.append(message)
        print(jsonToSend)
        response += json.dumps(jsonToSend)
        return response
    #TODO throw error






if __name__ == "__main__":
    main()
