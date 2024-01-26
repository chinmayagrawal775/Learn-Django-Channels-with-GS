from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('websocket connected...', event)
        self.send({
            'type':'websocket.accept',
        })
        
    def websocket_receive(self, event):
        print('websocket recieved...', event)
        print(event['text'])
        self.send({
            'type':'websocket.send',
            'text':'message sent to client'
        })

    def websocket_disconnect(self, event):
        print('websocket disconnected...', event)
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('websocket connected...', event)
        await self.send({
            'type':'websocket.accept',
        })

    async def websocket_receive(self, event):
        print('websocket recieved...', event)
        print(event['text'])
        await self.send({
            'type':'websocket.send',
            'text':'message sent to client'
        })

    async def websocket_disconnect(self, event):
        print('websocket disconnected...', event)
        raise StopConsumer()