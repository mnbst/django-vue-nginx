import json

from celery.result import AsyncResult
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from .settings import END_MESSAGE
from .tasks import scraping


class FetchConsumer(AsyncWebsocketConsumer):
    result = AsyncResult
    group_name = "scraping"

    async def connect(self):
        print("connected")
        await self.channel_layer.group_add(
            group=self.group_name,
            channel=self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print('disconnect', close_code)
        self.result.revoke(terminate=True)
        await self.channel_layer.group_discard(
            group=self.group_name,
            channel=self.channel_name
        )
        raise StopConsumer()

    async def receive(self, text_data=None, bytes_data=None):
        print("receive", text_data)
        await self.send(text_data='starting...')
        settings = json.loads(text_data)
        self.result = scraping.delay(settings=settings)

    async def scraping_messages(self, event):
        text = event["text"]
        await self.send(text_data=text)
        if text == END_MESSAGE:
            await self.send(close=True)
