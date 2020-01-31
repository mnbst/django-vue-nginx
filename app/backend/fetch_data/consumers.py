import asyncio
import json
from channels.consumer import AsyncConsumer
from .manage.youtubeAPI import FetchDataFromYoutube


class FetchDataConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print("receive", event['text'])
        data = json.loads(event['text'])
        fdfy = FetchDataFromYoutube(settings=data, ws=self)
        await fdfy.youtube_search()
        print(data)

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        await self.send({
            'type': 'websocket.send',
            'text': 'error occored'
        })
