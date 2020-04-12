import graphene

from .graphql.query.root import RootQuery
from .graphql.mutation.root import RootMutation

schema = graphene.Schema(
    query=RootQuery,
    mutation=RootMutation,
)
