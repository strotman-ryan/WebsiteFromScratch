'''
Implements web sockets
'''
import threading
import json
import asyncio
import websockets
from datetime import datetime

#TODO delete or use this
'''
message = urllib.parse.unquote_plus(message)

jsonToSend = []
for time, content in zip(times[messagesClientHas::], words[messagesClientHas::]):
    message = {}
    message["time"] = time
    message["message"] = content
    jsonToSend.append(message)
'''

class WebSocketServer(threading.Thread):

    def __init__(self, messages, network):
        self.messages = messages
        self.network = network
        self.users = set()   #all the websockets currently open
        threading.Thread.__init__(self)
        print("started websocket server")


    '''
    the main function that will set up the websockets and send and receive
    '''
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while(True):
            try:
                start_server = websockets.serve(self.handleMessages, self.network.ServerIp,self.network.WebsocketPortNum)
                #break if no error
                break
            except Exception as exc :
                self.network.WebsocketPortNum += 1
                print("Port failed to open for websockets")
                print(exc)
        loop.run_until_complete(start_server)
        loop.run_forever()

    async def register(self, socket):
        self.users.add(socket)
    
    async def unregister(self, socket):
        self.users.remove(socket)

    async def NotifyUsers(self, time, content):
        if self.users:
            jsonToSend = []
            message = {}
            message["time"] = time
            message["message"] = content
            jsonToSend.append(message)
            strJson = json.dumps(jsonToSend)
            await asyncio.wait([user.send(strJson) for user in self.users])

    async def handleMessages(self, websocket, path):
        print("socket connected to websocket")
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            async for message in websocket:
                time = str(datetime.now())
                self.messages.addMessage(time, message)
                await self.NotifyUsers(time, message)
        finally:
            await self.unregister(websocket)




