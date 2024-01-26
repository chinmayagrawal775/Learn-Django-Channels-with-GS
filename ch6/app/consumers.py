from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Chat, Group
import json

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('websocket connected...', event)
        print(self.channel_layer)
        print(self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send({
            'type':'websocket.accept',
        })
        
    def websocket_receive(self, event):
        print('websocket/message recieved from client...', event)
        print(event['text'])
        data = json.loads(event['text'])['msg']
        group = Group.objects.get(name=self.group_name)
        Chat(content=data, group=group).save()
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
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
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
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
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        data = json.loads(event['text'])['msg']
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        await database_sync_to_async(Chat(content=data, group=group).save())()
        await self.channel_layer.group_send(self.group_name, {
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
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()