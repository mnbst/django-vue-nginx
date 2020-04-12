import graphene

from .dictionary_console.schema.query.root import RootQuery
from .dictionary_console.schema.mutation.root import RootMutation

schema = graphene.Schema(
    query=RootQuery,
    mutation=RootMutation,
)
