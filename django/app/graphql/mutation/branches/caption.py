import graphene

from ...object_types import CaptionType, CaptionWordType, WordType
from ....dictionary_console.models import *
from django.db import transaction


class WordInput(graphene.InputObjectType):
    word_ini = graphene.String()
    word = graphene.String()
    meaning = graphene.String()


class CaptionWordInput(graphene.InputObjectType):
    id = graphene.ID()
    fixed_word = graphene.String()
    fixed_meaning = graphene.String()
    order = graphene.Int()

    def __str__(self):
        return self.fixed_word


class CaptionInput(graphene.InputObjectType):
    id = graphene.ID()
    index = graphene.Int()
    text = graphene.String()
    start_time = graphene.Int()
    end_time = graphene.Int()


class SaveCaption(graphene.Mutation):
    caption = graphene.Field(CaptionType)

    class Arguments:
        caption_input = CaptionInput(required=True)
        caption_word_inputs = graphene.List(CaptionWordInput)
        word_inputs = graphene.List(WordInput)

    @staticmethod
    def _save_word_inputs(word_inputs: [Word]):
        if not word_inputs:
            return
        for word in word_inputs:
            try:
                instance: Word = Word.objects.get(word=word.word)
            except Word.DoesNotExist:
                continue
            instance.meaning = word.meaning
            instance.save()

    @staticmethod
    def _save_caption_word_inputs(caption_word_inputs: [CaptionWord]):
        if not caption_word_inputs:
            return
        fixed_words = list(
            input_object.fixed_word for input_object in caption_word_inputs
        )
        caption_word_id = caption_word_inputs[0].id
        caption_word_set = CaptionWord.objects.get(
            id=caption_word_id
        ).caption.captionword_set.all()
        if len(caption_word_set) > len(caption_word_inputs):
            for caption_word in caption_word_set:
                str_caption_word = str(caption_word)
                if str_caption_word not in fixed_words:
                    caption_word.delete()
        for caption_word in caption_word_inputs:
            instance: CaptionWord = CaptionWord.objects.get(id=caption_word.id)
            instance.fixed_word = caption_word.fixed_word
            instance.fixed_meaning = caption_word.fixed_meaning
            instance.order = caption_word.order
            instance.save()

    @classmethod
    def mutate(cls, *args, **kwargs):
        caption_input = kwargs["caption_input"]
        caption_word_inputs: [CaptionWord] = (
            kwargs["caption_word_inputs"] if "caption_word_inputs" in kwargs else None
        )
        word_inputs: [Word] = kwargs["word_inputs"] if "word_inputs" in kwargs else None
        with transaction.atomic():
            cls._save_word_inputs(word_inputs)
            cls._save_caption_word_inputs(caption_word_inputs)
            instance: Caption = Caption.objects.get(id=caption_input.id)
            instance.text = caption_input.text
            instance.start_time = caption_input.start_time
            instance.end_time = caption_input.end_time
            instance.save()
        return cls(caption=instance)
