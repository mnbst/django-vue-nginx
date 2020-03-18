import json

from asgiref.sync import async_to_sync
from celery.result import AsyncResult
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

from .settings import END_MESSAGE
from .tasks import scraping


class FetchConsumer(WebsocketConsumer):
    result = AsyncResult
    group_name = "fetch"

    def connect(self):
        print("connected")
        async_to_sync(self.channel_layer.group_add)(
            group=self.group_name,
            channel=self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print('disconnect', close_code)
        self.result.revoke(terminate=True)
        async_to_sync(self.channel_layer.group_discard)(
            group=self.group_name,
            channel=self.channel_name
        )
        raise StopConsumer()

    def receive(self, text_data=None, bytes_data=None):
        print("receive", text_data)
        self.send(text_data='starting...')
        settings = json.loads(text_data)
        self.result = scraping.delay(settings=settings)

    def fetch_messages(self, event):
        text = event["text"]
        self.send(text_data=text)
        if text == END_MESSAGE:
            self.send(close=True)
