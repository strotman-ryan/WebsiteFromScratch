
import os
import threading


#class for loggin information to a file
#multiple thread will be using the same file so must synchronize
class Logging:

    lock = threading.Lock()
    fileName = os.path.dirname(os.path.realpath(__file__)) + "/log.txt"

    @staticmethod
    def WriteToLog(logMessage):
        Logging.lock.acquire()
        print(logMessage)
        with open(Logging.fileName, "a") as logFile:
            logFile.write(str(logMessage))
            logFile.write('\n')
        Logging.lock.release()
    

