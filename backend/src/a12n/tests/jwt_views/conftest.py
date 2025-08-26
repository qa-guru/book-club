import factory
import pytest
from pytest_factoryboy import register
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = "jwt-tester-user"

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password("sn00pd0g")
        if create:
            self.save()


register(UserFactory)


@pytest.fixture
def initial_token_pair(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}
