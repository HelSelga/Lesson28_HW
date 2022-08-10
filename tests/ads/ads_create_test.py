import pytest


@pytest.mark.django_db
def test_ads_create(client, user, category):
    response = client.post(
        "/ads/create/",
        {
            "name": "new test ad",
            "price": 20,
            "is_published": False,
            "description": "test description",
            "author": user.id,
            "category": category.id
        },
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.data == {
        "id": 1,
        "description": "test description",
        "author": user.id,
        "category": category.id,
        "image": None,
        "name": "new test ad",
        "price": 20,
        "is_published": False
    }
