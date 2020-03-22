from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url

from . import settings
from .consumers import FetchConsumer, DebugFetchConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^(?P<realtime>[\w.@+-]+)", DebugFetchConsumer) if settings.DEBUG_CELERY else url(
                        r"^(?P<realtime>[\w.@+-]+)", FetchConsumer)
                ]
            )
        )
    )
})
