import pytest
from aiodanbooru import DanbooruAPI, DanbooruPost


@pytest.mark.asyncio
async def test_get_posts():
    api = DanbooruAPI(base_url="https://danbooru.donmai.us")
    tags = ["cat_girl", "solo"]
    limit = 10

    posts = await api.get_posts(tags=tags, limit=limit)

    assert len(posts) <= limit
    for post in posts:
        assert post.tag_string is not None
        assert post.image_width > 0
        assert post.image_height > 0


@pytest.mark.asyncio
async def test_get_media():
    api = DanbooruAPI(base_url="https://danbooru.donmai.us")
    tags = ["cat_girl", "solo"]
    limit = 1

    posts = await api.get_posts(tags=tags, limit=limit)

    assert len(posts) == 1
    post = posts[0]

    # Testing image retrieval
    if post.is_image():
        media_data = await post.get_media()
        assert isinstance(media_data, bytes)
        assert len(media_data) > 0

    # Testing video retrieval
    if post.is_video():
        media_data = await post.get_media(use_large=False)
        assert isinstance(media_data, bytes)
        assert len(media_data) > 0


@pytest.mark.asyncio
async def test_get_random_post():
    api = DanbooruAPI(base_url="https://danbooru.donmai.us")
    random_post = await api.get_random_post()
    assert random_post is not None
    assert isinstance(random_post, DanbooruPost)


# Running the tests
if __name__ == "__main__":
    pytest.main(["-v"])
