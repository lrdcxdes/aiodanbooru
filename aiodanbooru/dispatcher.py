import asyncio
from typing import List, Union

from aiodanbooru.api import DanbooruPost, DanbooruAPI
from aiodanbooru.base.filters import Filter
from aiodanbooru.base.handler import Handler


class Dispatcher:
    def __init__(self):
        self.queue = asyncio.Queue()
        self._handlers: List[Handler] = []
        self.api = DanbooruAPI()
        self.__last_post_id = None

    async def watch_posts(self):
        while True:
            await asyncio.sleep(0.02)
            post: DanbooruPost = (await self.api.get_posts(limit=1))[0]
            post_id = post.id
            if self.__last_post_id is None:
                self.__last_post_id = post_id
            elif post_id != self.__last_post_id:
                self.__last_post_id = post_id
                await self.queue.put(post)

    async def handle_events(self):
        while True:
            post = await self.queue.get()
            for handler in self._handlers:
                if await handler.check(post) is False:
                    continue
                if asyncio.iscoroutinefunction(handler.func):
                    await handler.func(post)
                else:
                    handler.func(post)
            self.queue.task_done()

    def new_post(self, filters: Union[List[Filter], Filter] = None):
        def wrapper(func):
            self._handlers.append(Handler(func, filters))
            return func

        return wrapper

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.watch_posts())
        loop.create_task(self.handle_events())
        loop.run_forever()


if __name__ == "__main__":
    from aiodanbooru.base import filters

    dispatcher = Dispatcher()

    @dispatcher.new_post(filters.all)
    async def handle_new_post(post_id):
        print(f"New post with ID {post_id} has appeared on the site!")

    dispatcher.start()
