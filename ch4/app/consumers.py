from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('websocket connected...', event)
        print(self.channel_layer)
        print(self.channel_name)
        async_to_sync(self.channel_layer.group_add)('programmers', self.channel_name)
        self.send({
            'type':'websocket.accept',
        })
        
    def websocket_receive(self, event):
        print('websocket/message recieved from client...', event)
        print(event['text'])
        async_to_sync(self.channel_layer.group_send)('programmers', {
            'type': 'chat.message',
            'message': event['text']
        })
    
    def chat_message(self, event):
        print(event)
        print(event['message'])
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    def websocket_disconnect(self, event):
        print('websocket disconnected...', event)
        print(self.channel_layer)
        print(self.channel_name)
        async_to_sync(self.channel_layer.group_discard)('programmers', self.channel_name)
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('websocket connected...', event)
        print(self.channel_layer)
        print(self.channel_name)
        await self.channel_layer.group_add('programmers', self.channel_name)
        await self.send({
            'type':'websocket.accept',
        })
        
    async def websocket_receive(self, event):
        print('websocket/message recieved from client...', event)
        print(event['text'])
        await self.channel_layer.group_send('programmers', {
            'type': 'chat.message',
            'message': event['text']
        })
    
    async def chat_message(self, event):
        print(event)
        print(event['message'])
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    async def websocket_disconnect(self, event):
        print('websocket disconnected...', event)
        print(self.channel_layer)
        print(self.channel_name)
        await self.channel_layer.group_discard('programmers', self.channel_name)
        raise StopConsumer()