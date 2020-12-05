import graphene

from ....dictionary_console.models import CaptionWord, Word
from ...object_types import CaptionWordType


class SaveCaptionWord(graphene.Mutation):
    caption_word = graphene.Field(CaptionWordType)

    class Arguments:
        caption_word_id = graphene.ID(required=True)
        root_word_id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, *args, **kwargs):
        caption_word_id = kwargs.get("caption_word_id")
        root_word_id = kwargs.get("root_word_id")
        instance: CaptionWord = CaptionWord.objects.get(id=caption_word_id)
        instance.root_word = Word.objects.get(id=root_word_id)
        instance.save()
        return cls(caption_word=instance)
