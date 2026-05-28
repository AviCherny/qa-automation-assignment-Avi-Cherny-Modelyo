import pytest
import allure
from api.clients.posts_client import get_posts, get_post


@pytest.mark.api
@allure.feature("Posts")
@allure.story("GET /posts")
def test_get_posts_returns_list(session):
    response = get_posts(session)
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 100


@pytest.mark.api
@allure.feature("Posts")
@allure.story("GET /posts")
def test_get_post_item_has_expected_schema(session):
    post = get_posts(session).json()[0]

    assert isinstance(post["userId"], int)
    assert isinstance(post["id"], int)
    assert isinstance(post["title"], str) and post["title"]
    assert isinstance(post["body"], str) and post["body"]


@pytest.mark.api
@allure.feature("Posts")
@allure.story("GET /posts/{id}")
def test_get_post_by_valid_id_returns_correct_post(session):
    response = get_post(session, 1)
    post = response.json()

    assert response.status_code == 200
    assert post["id"] == 1
    assert "userId" in post
    assert "title" in post
    assert "body" in post


@pytest.mark.api
@allure.feature("Posts")
@allure.story("GET /posts/{id}")
def test_get_post_nonexistent_id_returns_404(session):
    response = get_post(session, 99999)

    assert response.status_code == 404
