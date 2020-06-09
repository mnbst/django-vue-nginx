import json

from asgiref.sync import async_to_sync
from celery.result import AsyncResult
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from .scraping.tasks import get_list, get_caption
from ..settings import END_MESSAGE


class GetVideoListConsumer(AsyncWebsocketConsumer):
    result = AsyncResult
    group_name = "get_video_list"

    async def connect(self):
        print("connected")
        await self.channel_layer.group_add(
            group=self.group_name, channel=self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print("receive", text_data)
        settings = json.loads(text_data)
        self.result = get_list.delay(settings=settings)

    async def disconnect(self, close_code):
        print("disconnect", close_code)
        self.result.revoke(terminate=True)
        await self.channel_layer.group_discard(
            group=self.group_name, channel=self.channel_name
        )
        raise StopConsumer()

    async def get_video_list_messages(self, event):
        if "text" in event:
            text = event["text"]
            if text == END_MESSAGE:
                await self.send(close=True)
                return
            await self.send(text_data=text)
        if "data" in event:
            data = event["data"]
            await self.send(data)


class DebugGetVideoListConsumer(WebsocketConsumer):
    result = AsyncResult
    group_name = "get_video_list"

    def connect(self):
        print("connected")
        async_to_sync(self.channel_layer.group_add)(
            group=self.group_name, channel=self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print("disconnect", close_code)
        self.result.revoke(terminate=True)
        async_to_sync(self.channel_layer.group_discard)(
            group=self.group_name, channel=self.channel_name
        )
        raise StopConsumer()

    def receive(self, text_data=None, bytes_data=None):
        print("receive", text_data)
        self.send(text_data="starting...")
        settings = json.loads(text_data)
        self.result = get_list.delay(settings=settings)

    def get_video_list_messages(self, event):
        text = event["text"]
        self.send(text_data=text)
        if text == END_MESSAGE:
            self.send(close=True)


class GetCaptionConsumer(AsyncWebsocketConsumer):
    result = AsyncResult
    group_name = "get_caption"

    async def connect(self):
        print("connected")
        await self.channel_layer.group_add(
            group=self.group_name, channel=self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None):
        print("receive", text_data)
        data = json.loads(text_data)
        self.result = get_caption.delay(data=data)

    async def disconnect(self, close_code):
        print("disconnect", close_code)
        self.result.revoke(terminate=True)
        await self.channel_layer.group_discard(
            group=self.group_name, channel=self.channel_name
        )
        raise StopConsumer()

    async def get_caption_messages(self, event):
        if "text" in event:
            text = event["text"]
            if text == END_MESSAGE:
                await self.send(close=True)
                return
            await self.send(text_data=text)
        if "data" in event:
            data = event["data"]
            await self.send(data)


class DebugGetCaptionConsumer(WebsocketConsumer):
    result = AsyncResult
    group_name = "get_caption"

    def connect(self):
        print("connected")
        async_to_sync(self.channel_layer.group_add)(
            group=self.group_name, channel=self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print("disconnect", close_code)
        self.result.revoke(terminate=True)
        async_to_sync(self.channel_layer.group_discard)(
            group=self.group_name, channel=self.channel_name
        )
        raise StopConsumer()

    def receive(self, text_data=None):
        print("receive", text_data)
        self.send(text_data="starting...")
        data = json.loads(text_data)
        self.result = get_caption.delay(data=data)

    def get_caption_messages(self, event):
        text = event["text"]
        self.send(text_data=text)
        if text == END_MESSAGE:
            self.send(close=True)
