=============
Danbooru Library
=============

.. image:: https://img.shields.io/pypi/v/aiodanbooru.svg
        :target: https://pypi.org/project/aiodanbooru/
        :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/aiodanbooru.svg
        :target: https://pypi.org/project/aiodanbooru/
        :alt: Python Versions

Overview
========

Danbooru is a Python library for interacting with the Danbooru API. It provides a simple and convenient way to retrieve posts, download media files, and perform various operations on Danbooru posts.

Features
========

- Retrieve posts based on tags.
- Download images and videos.
- Get random posts.
- Perform advanced search queries.
- And more!

Installation
============

You can install Danbooru using pip:

::

    $ pip install aiodanbooru

Usage
=====

Here's a simple example that demonstrates how to use Danbooru:

::

    from danbooru import DanbooruAPI

    api = DanbooruAPI(base_url="https://danbooru.donmai.us")
    posts = await api.get_posts(tags=["cat_girl", "solo"], limit=10)

    if posts:
        post = posts[0]
        media_data = await post.get_media()
        with open(post.filename, "wb") as file:
            file.write(media_data)
        print("Media saved!")


For more details and advanced usage examples, please refer to the `documentation <https://aiodanbooru.readthedocs.io/en/latest/>`_.

Contributing
============
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on the `GitHub repository <https://github.com/lrdcxdes/aiodanbooru>`_.


License
=======
Danbooru is licensed under the MIT license. See the `LICENSE <https://github.com/lrdcxdes/aiodanbooru/blob/main/LICENSE>`_ file for more details.
