
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

def createServer():
    try :
        serversocket = FindPortDynamically()
        serversocket.listen(5)
        while(1): 
            try:
                (clientsocket, address) = serversocket.accept()
            except Exception as e:
                print("socket accept failed")
                print(e)
                continue
            #TODO be able to receive large messages
            rd = clientsocket.recv(5000).decode()
            print(rd)
            httpMessage = HttpMessage(rd)
            httpMessage.Print()
            data =  HandleMessage(httpMessage)
            clientsocket.sendall(data.encode())
            clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt :
        print("\nShutting down...\n")
    except Exception as exc :
        print("Error:\n")
        print(exc)

    serversocket.close()

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

def HandleMessage(httpMessage):
    if httpMessage.command == "GET":
        return HandleGet(httpMessage)
    if httpMessage.command == "POST":
        return HandlePost(httpMessage)

def HandleGet(httpMessage):
    paths = httpMessage.path.split('=')
    if len(paths) == 2:
        return GetMessages(int(paths[1]))
    response = MakeStatus200()
    response += MakeHeader()
    response += MakeFile("main.html",{'counter':counter,'messages':zip(times[::-1],words[::-1])})
    response += new_line
    return response

def GetMessages(messagesClientHas):
    response = MakeStatus200()
    response += MakeHeader()
    print("1")
    for time, word in zip(times[messagesClientHas::], words[messagesClientHas::]):
        response += time + ',' + word + ';'
    print("2")
    response += new_line
    print("3")
    return response
    
def HandlePost(httpMessage):
    bodyArray =httpMessage.body.split('=')
    message = bodyArray[1]
    message = urllib.parse.unquote_plus(message)
    words.append(message)
    times.append(str(datetime.now()))

    response = "HTTP/1.1 303 See Other" + new_line
    response += "Location: " + "/" + new_line
    return response
    


#port_num and server_ip are global variables
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


createServer()


if __name__ == "__main__":
    createServer()
