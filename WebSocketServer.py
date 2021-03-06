'''
Implements web sockets
'''
import threading
import json
import asyncio
import websockets
from datetime import datetime
from DataBase.DataBase import DataBase
from TokenAuthentication import TokenAuthentication

class WebSocketServer(threading.Thread):

    def __init__(self,  network):
        self.network = network
        self.users = set()   #all the websockets currently open
        threading.Thread.__init__(self)
        self.setUpServer()
        print("started websocket server")


    '''
    finds the next open port for the websocket and sets it up
    '''
    def setUpServer(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        while(True):
            try:
                self.start_server = websockets.serve(self.handleMessages, self.network.ServerIp,self.network.WebsocketPortNum)
                #break if no error
                break
            except Exception as exc :
                self.network.WebsocketPortNum += 1
                print("Port failed to open for websockets")
                print(exc)

    '''
    the main function that starts the websocket
    '''
    def run(self):
        self.loop.run_until_complete(self.start_server)
        self.loop.run_forever()

    async def register(self, socket):
        self.users.add(socket)
    
    async def unregister(self, socket):
        self.users.remove(socket)

    async def NotifyUsers(self, user, content):
        if self.users:
            jsonToSend = []
            message = {}
            message["user"] = user
            message["message"] = content
            jsonToSend.append(message)
            strJson = json.dumps(jsonToSend)
            await asyncio.wait([user.send(strJson) for user in self.users])

    async def handleMessages(self, websocket, path):
        print("socket connected to websocket")
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            async for content in websocket:
                contentJson = json.loads(content)
                message =  contentJson["message"]
                valid, tokenBody = TokenAuthentication.DecodeToken(contentJson["Token"])
                if not valid:
                    #TODO close connection in this scenario
                    continue
                DataBase.GetInstance().AddMessage(message, tokenBody["UserName"])
                await self.NotifyUsers(tokenBody["UserName"], message)
        finally:
            await self.unregister(websocket)




