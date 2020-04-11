import graphene

from .dictionary_console.schema import Query

schema = graphene.Schema(
    query=Query,
)
