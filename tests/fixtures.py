import pytest


@pytest.fixture
@pytest.mark.django_db
def user_token(client, django_user_model):
    username = "Fixik"
    password = "23Ft/ghT^:sfR56"

    django_user_model.objects.create_user(username=username, password=password)
    response = client.post("/user/token/", {"username": username, "password": password}, format='json')

    return response.data["access"]
