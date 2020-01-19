from django.template.response import TemplateResponse
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Word
from .models import Caption
from .models import Video
from .models import VideoExcepted
from .serializers import WordSerializer
from .serializers import CaptionSerializer
from .serializers import VideoSerializer
from .serializers import VideoExceptedSerializer
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache


class WordView(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class CaptionView(viewsets.ModelViewSet):
    queryset = Caption.objects.all()
    serializer_class = CaptionSerializer


class VideoView(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoExceptedView(viewsets.ModelViewSet):
    queryset = VideoExcepted.objects.all()
    serializer_class = VideoExceptedSerializer
