
from Logging import Logging

class HttpMessage:

    #conuted as a memeber of the class
    new_line = "\r\n"

    '''
    These are the members
    command<string> -> 'GET', 'POST' //TODO change this to method
    path<string> -> the full url path sent in the request
    pathRoutes<list[string]> -> the route the url is on; ex "/hello/what?cool=ex&three=5" -> ['hello','what']
    urlArgs<dictionary{string, string}> -> the argument in the url; ex "/hello/what?cool=ex&three=5" -> {'cool':'ex','three':'5'}
    version<string> -> the http version number
    headers<dictionary{string, string}> -> all the headers in a dictionary
    cookies<dictionary{string, string}> -> all cookies sent over
    body<string> -> the whole body
    '''

    #will parse httpMessage
    #socket is a recently connected socket
    def __init__(self, socket):
        #TODO be able to receive large messages
        rawinput = socket.recv(5000).decode()
        Logging.WriteToLog("bytes received: " + str(len(rawinput)) + "\n")
        lines = rawinput.split(self.new_line)
        self.ParseFirstLine(lines[0])
        #parse headers
        headersLastLine = lines.index("")
        self.ParseHeaders(lines[1:headersLastLine])
        self.ParseBody(socket, lines[headersLastLine +1 ::])
        
        
    '''
    Parse the body of the request
    socket <socket> -> the socket connected to the client
    linesLeft <list<string>> the lines that havent been read yet; may be empty
    '''
    def ParseBody(self, socket, linesLeft):
        #could have an issue since I am not join back with newline
        self.body = ''.join(linesLeft)
        sizeOfBody = 0
        contentLenthHeader = "content-length"
        if contentLenthHeader in self.headers.keys():
            sizeOfBody = int(self.headers[contentLenthHeader])

        bytesLeftToBeSent = sizeOfBody - len(self.body)
        while bytesLeftToBeSent > 0:
            newBytes = socket.recv(bytesLeftToBeSent).decode()
            bytesLeftToBeSent -= len(newBytes)
            self.body += newBytes


    '''
    parses the body of an http post request into a dictionary of values
    returns <dict<string, string>> the post body
    '''
    def ParseBodyPost(self):
        bodyParams = self.body.split("&")
        paramDict = {}
        for param in bodyParams:
            paramParts = param.split("=")
            paramDict[paramParts[0]] = paramParts[1]
        return paramDict
        

    '''
    First line is a string representing the first line received from client
    '''
    def ParseFirstLine(self, firstLine):
        #parse first line
        firstLineParts = firstLine.split(' ')
        self.command = firstLineParts[0]
        self.path = firstLineParts[1]
        pathParts = self.path.split('?')
        self.pathRoutes = pathParts[0].split('/')[1::]
        self.urlArgs = {}
        if(len(pathParts) > 1):
            args = pathParts[1].split('&')
            for arg in args:
                argKeyValue = arg.split('=')
                self.urlArgs[argKeyValue[0]] = argKeyValue[1]
        self.version = firstLineParts[2]

    '''
    parses the headers into a dictionary
    headerList <list<string>> -> the headers
    '''
    def ParseHeaders(self,headerList):
        self.headers = {}
        for i in range(len(headerList)):
            header = headerList[i].split(":") 
            #make all headers fields lower case since headers are case insensitive
            self.headers[header[0].lower()] = ':'.join(header[1::])
        self.ParseCookies()

    '''
    Looks for cookes and populates the cookie member if there are anh
    '''
    def ParseCookies(self):
        self.cookies = {}
        if "cookie" in self.headers:
            cookies = self.headers["cookie"].split(";")
            for cookie in cookies:
                cookieParts = cookie.strip().split("=")
                self.cookies[cookieParts[0]] = cookieParts[1]



    def Print(self):
        Logging.WriteToLog('----------http message----------------')
        Logging.WriteToLog('command: ' + self.command)
        Logging.WriteToLog('path: ' + self.path)
        Logging.WriteToLog('pathRoute: ')
        Logging.WriteToLog(self.pathRoutes)
        Logging.WriteToLog('urlArgs: ')
        Logging.WriteToLog(self.urlArgs)
        Logging.WriteToLog('version: ' + self.version)
        Logging.WriteToLog('--headers--')
        for key, value in self.headers.items():
            Logging.WriteToLog(key + ": " + value)
            print()
        print('--cookies--')
        for key, value in self.cookies.items():
            print(key + " = " + value)
        print('--body--')
        print(self.body)
