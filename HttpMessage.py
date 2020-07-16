


class HttpMessage:

    #will parse httpMessage
    #httpMessage is a string of the whole message
    def __init__(self, httpMessage):
        lines = httpMessage.split('\n')
        #parse first line
        firstLine = lines[0].split(' ')
        self.command = firstLine[0]
        self.path = firstLine[1]
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
        print('version: ' + self.version)
        print('--headers--')
        for key, value in self.headers.items():
            print(key + ": " + value)
        print('--body--')
        print(self.body)
