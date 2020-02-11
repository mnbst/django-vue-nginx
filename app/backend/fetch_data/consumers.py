from channels.consumer import AsyncConsumer
from .manage.youtubeAPI import FetchDataFromYoutube


class FetchDataConsumer(AsyncConsumer):
    fetch = FetchDataFromYoutube

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, settings):
        print("receive", settings)
        self.fetch = FetchDataFromYoutube(settings=settings['text'], ws=self)
        await self.fetch.youtube_search()

    async def websocket_disconnect(self, event):
        print('disconnect', event)
        await self.send({
            "type": "websocket.disconnect"
        })
