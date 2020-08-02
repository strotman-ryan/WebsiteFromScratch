

#connects to a databse and does certain actions
import mysql.connector
import threading


#TODO can you have multiple cursor objects for same connection?
#with many theards? is it thread safe?
class DataBase:

    _singletonLock = threading.Lock()
    _instace = None

    @staticmethod
    def GetInstance():
        if DataBase._instace == None:
            with DataBase._singletonLock:
                if DataBase._instace == None:
                    DataBase()
        return DataBase._instace

    #This is a private constuctor
    def __init__(self):
        if DataBase._instace != None:
            raise Exception("This is a singleton. Call GetInstance()")
        else:
            print("Making DataBaseConnection")
            self.connection = self._connectToDataBase()
            DataBase._instace = self

    #connect to DB and return a cursor
    def _connectToDataBase(self):
        cnx = mysql.connector.connect(
            user='RyanUser',
            password='MakeThisStrongerForProduction1!',
            host='127.0.0.1',
            database='Website')
        return cnx


    def AddNewUser(self,userName, password):
        cursor = self.connection.cursor()
        add_user = ("INSERT INTO User "
               "(userName, password) "
               "VALUES (%s, %s)")
        cursor.execute(add_user, (userName, password))
        self.connection.commit()
        cursor.close()


    def ValidateUser(self, userName, password):
        getUser = """select userName, password
            from User
            where userName = %s and password = %s"""
        cursor = self.connection.cursor()
        cursor.execute(getUser,(userName,password))
        #results is a list of tuples
        results = cursor.fetchall()
        cursor.close()
        #check the result set has one and only one user
        if len(results):
            return True
        if len(results) == 0:
            return False
        raise Exception("Multiple users in Data Base with same username")

    '''
    adds a new message to the message table with the proper userId
    '''
    def AddMessage(self, message, userName):
        addMessage = '''insert into Messages (message, userId)
                        values(%s, 
                        (select id from User where userName = %s))'''
        cursor = self.connection.cursor()
        cursor.execute(addMessage,(message,userName))
        self.connection.commit()
        cursor.close()

    '''
    returns a list of tuples(message, user)
    message and user are strings
    '''
    def GetAllMessages(self):
        getAllMessages = '''
            select Messages.message, User.userName
            from Messages
            inner join User on Messages.userId = User.id;
            '''
        cursor = self.connection.cursor()
        cursor.execute(getAllMessages)
        results = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return results

#DataBase.GetInstance().AddNewUser("mattew", "pass word")
print(DataBase.GetInstance().GetAllMessages())
