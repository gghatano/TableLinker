import graphene
from django.contrib.auth.hashers import make_password
from graphql_jwt.decorators import login_required
from graphql_schema.types.objects import UserType, CreateUserInputType, UpdateUserInputType
from users.models import User

from django.db import transaction


class PasswordResetRequest(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    @transaction.atomic
    def mutate(
        cls, root, info, email,
    ):
        user = User.objects.filter(email=email)
        if not user:
            return None
        user[0].password_reset_request(email)
        return PasswordResetRequest(user=user[0])


class PasswordReset(graphene.Mutation):
    class Arguments:
        password_reset_token = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, password_reset_token, password):
        user = User.password_reset(password_reset_token, password)
        return PasswordReset(user=user)


class CreateUser(graphene.Mutation):
    class Arguments:
        input = CreateUserInputType(required=True)

    user = graphene.Field(UserType)

    @classmethod
    @transaction.atomic
    def mutate(
        cls, root, info, input,
    ):

        user = User()
        user.name = input["name"]
        user.email = input["email"]
        user.password = make_password(input["password"])
        user.save()

        subject = "TableLinker ユーザ登録のお知らせ"
        text = (
            "{} 様\nTableLinker ユーザ登録が完了しました。\n"
            "登録したメールアドレス {} とパスワードでログインしてください。\n"
        ).format(user.name, user.email)
        user.email_user(subject, text)

        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        input = UpdateUserInputType(required=True)

    user = graphene.Field(UserType)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate(
        cls, root, info, input,
    ):
        pk = info.context.user.id
        user = User.objects.get(pk=pk)

        if not user:
            return None

        for attr, value in input.items():
            if attr == "password":
                setattr(user, attr, make_password(value))
            else:
                setattr(user, attr, value)
        user.save()

        return UpdateUser(user=user)
