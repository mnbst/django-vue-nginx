import graphene

from ....dictionary_console.models import *

class SettingsInput(graphene.InputObjectType):
    id = graphene.Int()
    authority = graphene.String()
    excepted_href = graphene.List(graphene.String)
    page_to_crawl = graphene.String()
    language_limit = graphene.Int()
    minimum_sentence = graphene.Int()
    video_per_page = graphene.Int()
    video_to_delete = graphene.List(graphene.String)
    video_to_renewal = graphene.List(graphene.String)


class CreateSettings(graphene.Mutation):
    id = graphene.Int()
    authority = graphene.String()
    excepted_href = graphene.List(graphene.String)
    page_to_crawl = graphene.String()
    language_limit = graphene.Int()
    minimum_sentence = graphene.Int()
    video_per_page = graphene.Int()
    video_to_delete = graphene.List(graphene.String)
    video_to_renewal = graphene.List(graphene.String)

    class Arguments:
        settings_input = SettingsInput(required=True)

    def mutate(self, info, settings_input):
        settings = FetchSetting(id=settings_input['id'],
                                authority=settings_input['authority'],
                                excepted_href=settings_input['excepted_href'],
                                page_to_crawl=settings_input['page_to_crawl'],
                                language_limit=settings_input['language_limit'],
                                minimum_sentence=settings_input['minimum_sentence'],
                                video_per_page=settings_input['video_per_page'],
                                video_to_delete=settings_input['video_to_delete'],
                                video_to_renewal=settings_input['video_to_renewal'],
                                )
        settings.save()

        return CreateSettings(id=settings.id,
                              authority=settings.authority,
                              excepted_href=settings.excepted_href,
                              page_to_crawl=settings.page_to_crawl,
                              language_limit=settings.language_limit,
                              minimum_sentence=settings.minimum_sentence,
                              video_per_page=settings.video_per_page,
                              video_to_delete=settings.video_to_delete,
                              video_to_renewal=settings.video_to_renewal, )