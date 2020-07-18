import threading

'''
Holds a list of messages and there corresponding times
self.messages <list<string>>: the content of each item
self.messages <list<string>>: the datetime that each message was received
the index of each list are related to each other
'''
class  Messages:


    def __init__(self):
        self.messages= []
        self.dateTimes = []
        self.lock = threading.Lock()

    '''
    dateTime <string>: assume datetime is unique
    content <string>
    '''
    def addMessage(self, dateTime,content):
        self.lock.acquire()
        self.dateTimes.append(dateTime)
        self.messages.append(content)
        self.lock.release()

    '''
    returns copies of all messages
    '''
    def GetAllMessages(self):
        self.lock.acquire()
        retObj = self.messages.copy(), self.dateTimes.copy()
        self.lock.release()
        return retObj
