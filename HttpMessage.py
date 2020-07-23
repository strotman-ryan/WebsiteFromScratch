


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
    body<string> -> the whole body
    '''

    #will parse httpMessage
    #socket is a recently connected socket
    def __init__(self, socket):
        #TODO be able to receive large messages
        rawinput = socket.recv(5000).decode()
        print("bytes received: " + str(len(rawinput)) + "\n")
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
        print("Number of bytes in body init read: " + str(len(self.body)))
        sizeOfBody = 0
        contentLenthHeader = "content-length"
        if contentLenthHeader in self.headers.keys():
            sizeOfBody = int(self.headers[contentLenthHeader])

        bytesLeftToBeSent = sizeOfBody - len(self.body)
        while bytesLeftToBeSent > 0:
            newBytes = socket.recv(bytesLeftToBeSent).decode()
            print("Read " + str(len(newBytes)) + " bytes")
            bytesLeftToBeSent -= len(newBytes)
            self.body += newBytes
        

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


    def Print(self):
        print('----------http message----------------')
        print('command: ' + self.command)
        print('path: ' + self.path)
        print('pathRoute: ')
        print(self.pathRoutes)
        print('urlArgs: ')
        print(self.urlArgs)
        print('version: ' + self.version)
        print('--headers--')
        for key, value in self.headers.items():
            print(key + ": " + value)
        print('--body--')
        print(self.body)
