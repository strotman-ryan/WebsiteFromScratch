

#connects to a databse and does certain actions
import mysql.connector
import threading
import hashlib 
import os
import bcrypt

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


    '''
    Tries to add a new user
    return <boolean> True if successful; false if not
    Note: will fail if userName is not unique
    '''
    def AddNewUser(self,userName, password):
        cursor = self.connection.cursor()
        add_user = ("INSERT INTO User "
               "(userName, password) "
               "VALUES (%s, %s)")
        try:            
            cursor.execute(add_user, (userName, self.get_hashed_password(password.encode())))
        except Exception as e:
            print("Error adding User: " + userName + "\n" + str(e))
            cursor.close()
            return False
        self.connection.commit()
        cursor.close()
        return True

    def get_hashed_password(self,plain_text_password):
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password, bcrypt.gensalt(12))

    def check_password(self, plain_text_password, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())

    def GetUsersPassword(self, userName):
        getPassword = """select password
            from User
            where userName = %s"""
        cursor = self.connection.cursor()
        cursor.execute(getPassword,(userName,))
        results = cursor.fetchall()
        cursor.close()
        #check the result set has one and only one user
        if len(results) > 1:
            #this should never happen
            raise Exception("Multiple users in Data Base with same username")
        if len(results) == 0:
            return None
        return results[0][0]

    def ValidateUser(self, userName, password):
        hashedPassword = self.GetUsersPassword(userName)
        print(hashedPassword)
        if hashedPassword != None:
            return self.check_password(password, hashedPassword)
        return False

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
    returns a list of tuples(message, user, timeOfMessage)
    message and user are strings
    '''
    def GetAllMessages(self):
        getAllMessages = '''
            select Messages.message, User.userName, Messages.date_time
            from Messages
            inner join User on Messages.userId = User.id;
            '''
        cursor = self.connection.cursor()
        cursor.execute(getAllMessages)
        results = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return results

#DataBase.GetInstance().AddNewUser("bob2", "hello")
print(DataBase.GetInstance().ValidateUser("bob2","hello"))