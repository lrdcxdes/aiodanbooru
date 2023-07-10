# Danbooru

[![PyPI](https://img.shields.io/pypi/v/aiodanbooru.svg)](https://pypi.org/project/aiodanbooru/)
[![License](https://img.shields.io/pypi/l/aiodanbooru.svg)](https://github.com/lrdcxdes/aiodanbooru/blob/main/LICENSE)

Danbooru is a Python library that provides an easy-to-use interface for interacting with the Danbooru API. It allows you to search for posts, retrieve post details, and download media files from the Danbooru image board.

## Features

- Simple and intuitive API for interacting with the Danbooru API
- Retrieve posts based on tags and limit
- Download media files (images, videos) associated with the posts
- Supports asynchronous requests using aiohttp

## Installation

You can install Danbooru using pip:
```bash
pip install aiodanbooru
```

## Usage

Here's a simple example that demonstrates how to use the Danbooru library:

```python
from aiodanbooru.api import DanbooruAPI
import aiodanbooru

async def main():
    api = DanbooruAPI(base_url="https://danbooru.donmai.us")

    posts = await api.get_posts(tags=["cat_girl", "solo"], limit=10)
    if posts:
        post = posts[0]
        media_data = await post.get_media()
        with open(post.filename, "wb") as file:
            file.write(media_data)
        print("Media file saved!")

aiodanbooru.run(main)
```

For more details and advanced usage examples, please refer to the **[documentation](https://aiodanbooru.readthedocs.io/en/latest/)**.

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on the **[GitHub repository](https://github.com/lrdcxdes/danbooru)**. Feel free to submit pull requests with improvements or fixes.

## License
This project is licensed under the MIT License. See the **[LICENSE](https://github.com/lrdcxdes/aiodanbooru/blob/main/LICENSE)** file for more information.
