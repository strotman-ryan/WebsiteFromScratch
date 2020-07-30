

from jinja2 import Template


class HttpResponseBuilder:
    '''
    A utility to class to make http responses easy to build
    '''
    newline = "\r\n"

    #key <string> the header key
    #value <string> the value of the key
    @staticmethod
    def AddHeader(key, value):
        return key + ": " + value + HttpResponseBuilder.newline

    '''
    Builds a string rep of a http header based off a dictionary of values
    headerDictionary<dict<string,string>> 
    note: the end of the header needs an extra new line to signal the end
    '''
    @staticmethod
    def MakeHeader(headerDictionary):
        headerString = ''
        for header, value in headerDictionary.items():
            headerString += HttpResponseBuilder.AddHeader(header, value)
        headerString += HttpResponseBuilder.newline
        return headerString

    @staticmethod
    def MakeStatus200():
        return "HTTP/1.1 200 OK" + HttpResponseBuilder.newline 

    '''
    I honestly dont know why i use these headers
    '''
    @staticmethod
    def MakeGenericHeader():
        headerDictionary = {}
        headerDictionary["Content-Type"] = "text/html; charset=utf-8"
        return HttpResponseBuilder.MakeHeader(headerDictionary)

    '''
    reads the filepath and adds the params where needed
    filePath <string> the relative path to the file wanting to be send
    params <dictionary<string, anything>> the values to replace
        key -> what to replace
        value -> what to replace it with
    '''
    @staticmethod
    def MakeFile(filePath, params):
        file = open(filePath, "r")
        content = file.read()
        file.close()
        temp = Template(content)
        return temp.render(params)

    '''
    adds a set cookie header with the cookie name and value
    '''
    @staticmethod
    def AddCookieHeader(cookieName, cookieValue):
        return HttpResponseBuilder.AddHeader("Set-Cookie", cookieName + "=" + cookieValue)