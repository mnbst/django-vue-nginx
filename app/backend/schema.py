import graphene

from .dictionary_console.schema import Query


class QueryRoot(Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=QueryRoot,
)
