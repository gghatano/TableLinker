import graphene

from .queries import CurrentUserQuery


class Query(CurrentUserQuery, graphene.ObjectType):
    pass
