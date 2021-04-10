import graphene

from .graphql.mutation.mutation_root import RootMutation
from .graphql.query.query_root import RootQuery

schema = graphene.Schema(
    query=RootQuery,
    mutation=RootMutation,
)
