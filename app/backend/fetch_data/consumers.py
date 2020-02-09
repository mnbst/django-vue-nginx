import asyncio
import json

from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer

from .manage.youtubeAPI import FetchDataFromYoutube


class FetchDataConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, settings):
        print("receive", settings)
        fetch = FetchDataFromYoutube(settings=settings['text'], ws=self)
        await fetch.youtube_search()

    async def websocket_disconnect(self, code):
        print('disconnect', code)
        await self.send({
            "type": "websocket.disconnect"
        })
