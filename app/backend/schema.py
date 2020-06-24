import graphene

from .graphql.query.query_root import RootQuery
from .graphql.mutation.mutation_root import RootMutation

schema = graphene.Schema(
    query=RootQuery,
    mutation=RootMutation,
)
