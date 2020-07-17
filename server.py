
from socket import *
from jinja2 import Template
from datetime import datetime
from HttpMessage import HttpMessage
import urllib.parse

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
        serversocket = FindPortDynamically()
        try:
            serversocket.listen(5)
        except Exception as e :
            print("Error: " + e)
        while(1): 
            HandleRequest(serversocket)
    except KeyboardInterrupt :
        print("\nShutting down...\n")
    finally:
        serversocket.close()

#input <socket>: a socket that just stopped listening
def HandleRequest(socket):
    try:
        (clientsocket, address) = socket.accept()
    except Exception as e:
        print("socket accept failed" + e)
        return
    #TODO be able to receive large messages
    rawinput = clientsocket.recv(5000).decode()
    httpMessage = HttpMessage(rawinput)
    httpMessage.Print()
    data = HandleMessage(httpMessage)
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
def HandleMessage(httpMessage):
    #first handle the path 
    #splits the path into its parts
    pathRoutes = httpMessage.pathRoutes
    if pathRoutes[0] in ['','index','favicon.ico']:
        return ServeIndex(httpMessage)
    if pathRoutes[0] in ['messages']:
        return ServeMessages(httpMessage)
    #TODO send 403 error message

#serves a request that is looking for index
def ServeIndex(httpMessage):
    if httpMessage.command == 'GET':
        response = MakeStatus200()
        response += MakeHeader()
        response += MakeFile("main.html",{'counter':counter,'messages':zip(times[::-1],words[::-1])})
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
    #TODO make it so it only handles a get request
    response = MakeStatus200()
    response += MakeHeader()
    messagesClientHas = int(httpMessages.urlArgs['numMessages'])
    for time, word in zip(times[messagesClientHas::], words[messagesClientHas::]):
        response += time + ',' + word + ';'
    response += new_line
    return response

#finds a port that is open and returns a binded socket
#socket used Steam (TCP)
def FindPortDynamically():
    try_port_num = port_num
    while(True):
        try:
            serversocket = socket(AF_INET, SOCK_STREAM)
            serversocket.bind((server_ip,try_port_num)) # this is the line that fails
            print('Access http://' + server_ip + ':' + str(try_port_num))
            return serversocket
        except Exception as exc :
            print("Error Finding port " +str(try_port_num) +":\n")
            print(exc)
            try_port_num += 1



if __name__ == "__main__":
    main()
