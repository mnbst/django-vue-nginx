import graphene
from graphene_django import DjangoObjectType

from ...dictionary_console.models import *


class WordType(DjangoObjectType):
    class Meta:
        model = Word


class VideoType(DjangoObjectType):
    class Meta:
        model = Video


class FetchSettingsType(DjangoObjectType):
    class Meta:
        model = FetchSetting


class RootQuery(graphene.ObjectType):
    word = graphene.List(WordType,
                         word_ini=graphene.String(),
                         word=graphene.String())
    video = graphene.List(VideoType,
                          video_genre=graphene.String(),
                          video_title=graphene.String())

    settings = graphene.Field(FetchSettingsType, authority=graphene.String())

    def resolve_word(self, info, **kwargs):
        word_ini = kwargs.get('word_ini')
        word = kwargs.get('word')
        if word_ini and not word:
            return Word.objects.order_by('word').filter(word_ini=word_ini).all()
        elif word:
            return Word.objects.order_by('word').filter(word=word).all()
        else:
            return Word.objects.order_by('word').filter()[:50].all()

    def resolve_video(self, info, **kwargs):
        title = kwargs.get('video_title')
        genre = kwargs.get('video_genre')
        if title and not genre:
            return Video.objects.filter(video_title__icontains=title)
        elif genre:
            return Video.objects.filter(video_genre__in=genre)
        else:
            return Video.objects.filter()[:50].all()

    def resolve_settings(self, info, **kwargs):
        authority = kwargs.get('authority')
        if authority:
            return FetchSetting.objects.get(authority=authority)
        return None