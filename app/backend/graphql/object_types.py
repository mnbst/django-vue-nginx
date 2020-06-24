from graphene_django import DjangoObjectType

from ..dictionary_console.models import *


class WordType(DjangoObjectType):
    class Meta:
        model = Word


class VideoType(DjangoObjectType):
    class Meta:
        model = Video


class CaptionType(DjangoObjectType):
    class Meta:
        model = Caption


class CaptionWordType(DjangoObjectType):
    class Meta:
        model = CaptionWord


class FetchSettingsType(DjangoObjectType):
    class Meta:
        model = FetchSetting
