import factory.django

from ads.models import AdModel, CategoryModel
from users.models import User


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryModel

    slug = factory.Faker('text')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    email = factory.Faker('email')


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdModel

    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
    price = 40
