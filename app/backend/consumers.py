import json

from asgiref.sync import async_to_sync
from celery.result import AsyncResult
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

from .celery import scraping


class FetchConsumer(WebsocketConsumer):
    result = AsyncResult
    group_name = 'scraping'

    def websocket_connect(self, event):
        print("connected", event)
        async_to_sync(self.channel_layer.group_add)(
            group=self.group_name,
            channel=self.channel_name
        )
        self.accept()

    def websocket_receive(self, settings):
        print("receive", settings)
        self.send(text_data='starting...')
        settings = json.loads(settings['text'])
        self.result = scraping.delay(settings=settings)
        # scraping(settings=settings,
        #          group_name=self.group_name)
        self.result.revoke(terminate=True)
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "fetch.messages",
            "message": 'message',
        })
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()

    def websocket_disconnect(self, event):
        print('disconnect', event)
        self.result.revoke(terminate=True)
        raise StopConsumer()

    def fetch_messages(self, event):
        async_to_sync(self.send)(text_data=event["message"])
