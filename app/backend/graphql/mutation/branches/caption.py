import graphene

from ...object_types import CaptionType


class CaptionInput(graphene.InputObjectType):
    id = graphene.ID()
    start_time = graphene.Int()
    end_time = graphene.Int()


class SaveCaption(graphene.Mutation):
    caption = graphene.Field(CaptionType)

    class Arguments:
        caption_input = CaptionInput(required=True)

    @classmethod
    def mutate(cls, *args, **kwargs):
        caption_input = kwargs["caption_input"]
        print(caption_input)
