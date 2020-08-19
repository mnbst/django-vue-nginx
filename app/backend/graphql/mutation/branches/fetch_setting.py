import graphene

from ....dictionary_console.models import *


class SettingsInput(graphene.InputObjectType):
    id = graphene.Int()
    authority = graphene.String()
    excepted_href = graphene.List(graphene.String)
    page_to_crawl = graphene.Int()
    language_limit = graphene.Int()
    minimum_sentence = graphene.Int()
    video_per_page = graphene.Int()
    video_to_delete = graphene.List(graphene.String)
    video_to_renewal = graphene.List(graphene.String)


class CreateSettings(graphene.Mutation):
    id = graphene.Int()
    authority = graphene.String()
    excepted_href = graphene.List(graphene.String)
    page_to_crawl = graphene.Int()
    language_limit = graphene.Int()
    minimum_sentence = graphene.Int()
    video_per_page = graphene.Int()
    video_to_delete = graphene.List(graphene.String)
    video_to_renewal = graphene.List(graphene.String)

    class Arguments:
        settings_input = SettingsInput(required=True)

    def mutate(self, info, settings_input):
        settings = FetchSetting.objects.get(id=settings_input["id"])
        settings.excepted_href = settings_input.excepted_href
        settings.page_to_crawl = settings_input.page_to_crawl
        settings.language_limit = settings_input.language_limit
        settings.minimum_sentence = settings_input.minimum_sentence
        settings.video_per_page = settings_input.video_per_page
        settings.video_to_delete = settings_input.video_to_delete
        settings.video_to_renewal = settings_input.video_to_renewal
        settings.save()
        return settings
