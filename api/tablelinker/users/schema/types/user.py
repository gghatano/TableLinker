from graphene_django import DjangoObjectType

from ...models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ["name", "email"]
