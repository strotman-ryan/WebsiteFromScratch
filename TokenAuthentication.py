
import jwt

'''
handles all token encoding and decoding
'''
class TokenAuthentication:

    _seceretKey = "TODO change this so get from system"

    '''
    Creates a JWT from a json obj
    '''
    @staticmethod
    def CreateToken(body):
        #decode converts bytes -> string
        return jwt.encode(body, TokenAuthentication._seceretKey, algorithm='HS256').decode("utf-8")

    '''
    Trys to decode the jwt
    if successful returns true and the token body as a dict
    if unsuccesful returns false and an empty dictionay
    '''
    @staticmethod
    def DecodeToken(token):
        try:
            token = jwt.decode(token, TokenAuthentication._seceretKey, algorithms=['HS256'])
            return True, token
        except Exception as e:
            print("Token not valid: " + str(e))
            return False, {}
    

