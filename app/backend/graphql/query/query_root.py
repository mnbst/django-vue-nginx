import graphene
from ..object_types import *
from ...dictionary_console.models import *


class RootQuery(graphene.ObjectType):
    words = graphene.List(WordType, word_ini=graphene.String(), word=graphene.String())
    video = graphene.Field(VideoType, video_href=graphene.String())
    video_list = graphene.List(
        VideoType,
        video_genre=graphene.List(graphene.String),
        vide_title=graphene.String(),
    )

    settings = graphene.Field(FetchSettingsType, authority=graphene.String())

    caption_list = graphene.List(CaptionType, video_href=graphene.String())

    def resolve_words(self, info, **kwargs):
        word_ini = kwargs.get("word_ini")
        word = kwargs.get("word")
        if word_ini and not word:
            return Word.objects.order_by("word").filter(word_ini=word_ini).all()
        elif word:
            return (
                Word.objects.order_by("word")
                .filter(word__istartswith=word, ng=False)[:20]
                .all()
            )
        else:
            return []

    def resolve_video(self, info, **kwargs):
        href = kwargs.get("video_href")
        if href:
            return Video.objects.filter(has_caption=True).get(video_href=href)
        return None

    def resolve_video_list(self, info, **kwargs):
        title = kwargs.get("video_title")
        genre = kwargs.get("video_genre")
        if title and not genre:
            return Video.objects.filter(video_title__icontains=title)
        elif genre:
            return Video.objects.filter(video_genre__in=genre)
        else:
            return Video.objects.all()

    def resolve_settings(self, info, **kwargs):
        authority = kwargs.get("authority")
        if authority:
            try:
                settings = FetchSetting.objects.get(authority=authority)
            except FetchSetting.DoesNotExist:
                settings = FetchSetting(
                    authority="super",
                    excepted_href=[],
                    page_to_crawl=1,
                    language_limit=1,
                    minimum_sentence=10,
                    video_per_page=1,
                    video_to_delete=[],
                    video_to_renewal=[],
                )
                settings.save()
            return settings
        return None
