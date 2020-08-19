import graphene
from ...object_types import WordType
from ....dictionary_console.models import Word


class SearchForWords(graphene.Mutation):
    words = graphene.List(WordType)

    class Arguments:
        word = graphene.String()

    @classmethod
    def mutate(cls, *args, **kwargs):
        word = kwargs.get("word")
        if not word:
            return []
        elif word:
            return cls(
                words=Word.objects.order_by("word")
                .filter(word__istartswith=word, ng=False)[:20]
                .all()
            )
