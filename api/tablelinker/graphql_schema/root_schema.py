from graphene import Schema
from graphql_schema.types.mutation_type import Mutation
from graphql_schema.types.query_type import Query

schema = Schema(query=Query, mutation=Mutation)
