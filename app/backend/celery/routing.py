from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url

from .consumers import GetVideoListConsumer, DebugGetVideoListConsumer, GetCaptionConsumer, DebugGetCaptionConsumer
from .. import settings

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^get_video_list",
                        DebugGetVideoListConsumer if settings.DEBUG_CELERY else GetVideoListConsumer),
                    url(r"^get_caption", DebugGetCaptionConsumer if settings.DEBUG_CELERY else GetCaptionConsumer)
                ]
            )
        )
    )
})
