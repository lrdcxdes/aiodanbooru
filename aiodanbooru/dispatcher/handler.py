import asyncio
from typing import Callable, Union, List

from aiodanbooru.dispatcher.filters import Filter
from aiodanbooru.models import DanbooruPost


class Handler(object):
    def __init__(self, func, filters: Union[List[Filter], Filter] = None):
        self.func: Callable = func
        self.filters: Union[List[Filter], Filter] = filters

    def __call__(self, post: DanbooruPost):
        return (
            self.func(post)
            if not asyncio.iscoroutinefunction(self.func)
            else asyncio.create_task(self.func(post))
        )

    async def check(self, post: DanbooruPost) -> bool:
        if self.filters is None:
            return True
        if isinstance(self.filters, list):
            for f in self.filters:
                if not await f(post):
                    return False
            return True
        return await self.filters(post)

    def __repr__(self):
        return f"<Handler func={self.func.__name__} filters={self.filters}>"
