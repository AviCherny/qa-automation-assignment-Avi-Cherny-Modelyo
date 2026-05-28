from config import API_BASE_URL


def posts_url() -> str:
    return f"{API_BASE_URL}/posts"


def post_url(post_id: int) -> str:
    return f"{API_BASE_URL}/posts/{post_id}"
