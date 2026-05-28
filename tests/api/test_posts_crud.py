import pytest
import allure
from api.clients.posts_client import create_post, update_post, delete_post


@pytest.mark.api
@allure.feature("Posts")
@allure.story("POST /posts")
def test_create_post_returns_201_with_generated_id(session):
    payload = {"title": "foo", "body": "bar", "userId": 1}

    response = create_post(session, payload)
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert "id" in data and isinstance(data["id"], int)


@pytest.mark.api
@allure.feature("Posts")
@allure.story("PUT /posts/{id}")
def test_update_post_returns_200_with_updated_body(session):
    payload = {"id": 1, "title": "updated title", "body": "updated body", "userId": 1}

    response = update_post(session, 1, payload)
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["id"] == 1


@pytest.mark.api
@allure.feature("Posts")
@allure.story("DELETE /posts/{id}")
def test_delete_post_returns_success(session):
    response = delete_post(session, 1)

    assert response.status_code in (200, 204)
