


class HttpMessage:
    '''
    These are the members
    command<string> -> 'GET', 'POST' //TODO change this to method
    path<string> -> the full url path sent in the request
    pathRoutes<list[string]> -> the route the url is on; ex "/hello/what?cool=ex&three=5" -> ['hello','what']
    urlArgs<dictionary{string, string}> -> the argument in the url; ex "/hello/what?cool=ex&three=5" -> {'cool':'ex','three':'5'}
    version<string> -> the http version number
    headers<dictionary{string}> -> all the headers in a dictionary
    body<string> -> the whole body
    '''

    #will parse httpMessage
    #httpMessage is a string of the whole message
    def __init__(self, httpMessage):
        lines = httpMessage.split('\n')
        #parse first line
        firstLine = lines[0].split(' ')
        self.command = firstLine[0]
        self.path = firstLine[1]
        pathParts = self.path.split('?')
        self.pathRoutes = pathParts[0].split('/')[1::]
        self.urlArgs = {}
        if(len(pathParts) > 1):
            args = pathParts[1].split('&')
            for arg in args:
                argKeyValue = arg.split('=')
                self.urlArgs[argKeyValue[0]] = argKeyValue[1]
        self.version = firstLine[2]
        #parse headers
        self.headers = {}
        lineMarker = 0
        for i in range(1,len(lines)):
            #check if end of header section
            if lines[i] == "\r":
                lineMarker = i + 1
                break 
            header = lines[i].split(":") 
            self.headers[header[0]] = header[1]
            
        #parse body
        self.body = ''.join(lines[lineMarker:])


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
