from factory import DjangoModelFactory, Faker

from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = Faker("name", locale="ja_JP")
    email = Faker("email")

    is_active = True
