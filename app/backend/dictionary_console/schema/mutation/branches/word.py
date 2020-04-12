import graphene

from ....models import Word


class WordInput(graphene.InputObjectType):
    id = graphene.Int()
    word_ini = graphene.String()
    word = graphene.String()
    meaning = graphene.String()


class CreateWord(graphene.Mutation):
    id = graphene.Int()
    word_ini = graphene.String()
    word = graphene.String()
    meaning = graphene.String()

    class Arguments:
        word_input = WordInput(required=True)

    def mutate(self, info, word_input):
        word = Word(id=word_input['id'],
                    word_ini=word_input['word_ini'],
                    word=word_input['word'],
                    meaning=word_input['meaning'])
        word.save()

        return CreateWord(id=word.id, word_ini=word.word_ini, word=word.word, meaning=word.meaning)
