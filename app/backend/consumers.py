import json

from celery.result import AsyncResult
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

from .tasks import scraping


class FetchDataConsumer(AsyncConsumer):
    result = AsyncResult
    group_name = 'scraping'

    async def websocket_connect(self, event):
        print("connected", event)
        await self.channel_layer.group_add(
            group=self.group_name,
            channel=self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, settings):
        print("receive", settings)
        await self.send({
            "type": "websocket.send",
            'text': 'starting...'
        })
        settings = json.loads(settings['text'])
        self.result = scraping.delay(
            settings=settings,
            group_name=self.group_name
        )
        raise StopConsumer()

    async def websocket_disconnect(self, event):
        print('disconnect', event)
        self.result.revoke()
        await self.channel_layer.group_discard(
            group=self.group_name,
            channel=self.channel_name
        )
        raise StopConsumer()

    async def fetch_data_message(self, event):
        await self.send({
            "type": "websocket.send",
            'text': event['text']
        })
