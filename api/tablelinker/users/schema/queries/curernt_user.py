import graphene

from ..types import UserType


class CurrentUserQuery(graphene.ObjectType):
    current_user = graphene.Field(UserType)

    def resolve_current_user(self, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
