from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf import settings
from django.conf.urls import url

from .consumers import (
    GetVideoListConsumer,
    DebugGetVideoListConsumer,
    GetCaptionConsumer,
    DebugGetCaptionConsumer,
)

application = ProtocolTypeRouter(
    {
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        url(
                            r"^get_video_list",
                            DebugGetVideoListConsumer.as_asgi()
                            if settings.DEBUG_CELERY
                            else GetVideoListConsumer,
                        ),
                        url(
                            r"^get_caption",
                            DebugGetCaptionConsumer.as_asgi()
                            if settings.DEBUG_CELERY
                            else GetCaptionConsumer,
                        ),
                    ]
                )
            )
        )
    }
)
