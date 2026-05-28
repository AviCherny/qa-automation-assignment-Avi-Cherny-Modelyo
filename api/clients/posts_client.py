import requests
from api.builders.url_builder import posts_url, post_url


def get_posts(session: requests.Session) -> requests.Response:
    return session.get(posts_url())


def get_post(session: requests.Session, post_id: int) -> requests.Response:
    return session.get(post_url(post_id))


def create_post(session: requests.Session, payload: dict) -> requests.Response:
    return session.post(posts_url(), json=payload)


def update_post(session: requests.Session, post_id: int, payload: dict) -> requests.Response:
    return session.put(post_url(post_id), json=payload)


def delete_post(session: requests.Session, post_id: int) -> requests.Response:
    return session.delete(post_url(post_id))
