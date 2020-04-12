import graphene

from .branches.fetch_setting import CreateSettings
from .branches.word import CreateWord


class RootMutation(graphene.ObjectType):
    create_word = CreateWord.Field()
    create_settings = CreateSettings.Field()
