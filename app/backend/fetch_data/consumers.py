import asyncio
import json
from channels.consumer import AsyncConsumer


class FetchDataConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            'type': 'websocket.accept'
        })
        await self.send({
            'type': 'websocket.send',
            'text':'hello world'
        })

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)
