
from DataBase.DataBase import DataBase #important to keep this as the first import!
from socket import SHUT_WR
from HttpResponseBuilder import HttpResponseBuilder
from datetime import datetime
from HttpMessage import HttpMessage
from Network import Network
import urllib.parse
import json
import threading 


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



    #parses the httpMessage and makes a response
    #input <httpMessage> = type HttpMssage and contains all the request information
    #output <string> = the http response to send back
    def HandleMessage(self,httpMessage):
        #first handle the path 
        #splits the path into its parts
        pathRoutes = httpMessage.pathRoutes
        if pathRoutes[0] in ['main','favicon.ico']:
            return self.ServeIndex(httpMessage)
        else:
            #default go to login screen
            return self.LoginHandler(httpMessage)
        #TODO send 403 error message

    #serves a request that is looking for index
    def ServeIndex(self, httpMessage):
        if httpMessage.command == 'GET':
            response = HttpResponseBuilder.MakeStatus200()
            response += HttpResponseBuilder.MakeGenericHeader()
            messages, dateTime = self.messages.GetAllMessages()
            params = {}
            params['messages'] = zip(dateTime[::-1],messages[::-1])
            params['ipAddress'] = self.network.ServerIp
            params['portNum'] = self.network.WebsocketPortNum
            response += HttpResponseBuilder.MakeFile("Views/main.html", params)
            response += HttpResponseBuilder.newline
            return response

    def LoginHandler(self, httpMessage):
        if httpMessage.command == 'GET':
            return self.ServeLoginPage()
        if httpMessage.command == 'POST':
            #check to make sure password is good
            #make token for user
            #redirect to main page
            info = httpMessage.body.split("&")
            userName = info[0].split('=')[1]
            password = info[1].split('=')[1]
            userName = urllib.parse.unquote_plus(userName)
            password = urllib.parse.unquote_plus(password)

            #check for valid user name and password
            dbInstance = DataBase.GetInstance()
            if dbInstance.ValidateUser(userName, password):
                response = "HTTP/1.1 303 See Other" + HttpResponseBuilder.newline
                response += "Location: " + "/main" + HttpResponseBuilder.newline
                response += HttpResponseBuilder.AddCookieHeader("password",password)
                response += HttpResponseBuilder.AddCookieHeader("userName", userName)
                return response
            else:
                return self.ServeLoginPage()

    def ServeLoginPage(self):
        response = HttpResponseBuilder.MakeStatus200()
        response += HttpResponseBuilder.MakeGenericHeader()
        response += HttpResponseBuilder.MakeFile("Views/login.html", {})
        response += HttpResponseBuilder.newline
        return response


