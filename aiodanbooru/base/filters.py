import inspect
from typing import Callable, Union, List

from aiodanbooru.models import DanbooruPost


class Filter:
    async def __call__(self, post: DanbooruPost):
        raise NotImplementedError

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)


class InvertFilter(Filter):
    def __init__(self, base):
        self.base = base

    async def __call__(self, post: DanbooruPost):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(post)
        else:
            x = self.base(post)

        return not x


class AndFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, post: DanbooruPost):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(post)
        else:
            x = self.base(post)

        # short circuit
        if not x:
            return False

        if inspect.iscoroutinefunction(self.other.__call__):
            y = await self.other(post)
        else:
            y = self.other(post)

        return x and y


class OrFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, post: DanbooruPost):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(post)
        else:
            x = self.base(post)

        # short circuit
        if x:
            return True

        if inspect.iscoroutinefunction(self.other.__call__):
            y = await self.other(post)
        else:
            y = self.other(post)

        return x or y


CUSTOM_FILTER_NAME = "CustomFilter"


def create(func: Callable, name: str = None, **kwargs) -> Filter:
    return type(
        name or func.__name__ or CUSTOM_FILTER_NAME,
        (Filter,),
        {"__call__": func, **kwargs},
    )()


# region all_filter
async def all_filter(_, __):
    return True


# noinspection PyShadowingBuiltins
all = create(all_filter)
"""Filter all messages."""


# endregion


# region author filter
# noinspection PyPep8Naming
class author(Filter, set):
    def __init__(self, users: Union[int, List[int]] = None):
        users = [] if users is None else users if isinstance(users, list) else [users]

        super().__init__(int(u) for u in users)

    async def __call__(self, post: DanbooruPost):
        return post.uploader_id in self


# endregion


# region tag filter
# noinspection PyPep8Naming
class tags(Filter, set):
    def __init__(self, *args: Union[str, List[str]]):
        _tags = []
        for arg in args:
            if isinstance(arg, list):
                _tags.extend(arg)
            else:
                _tags.append(arg)

        super().__init__(str(t) for t in _tags)

    async def __call__(self, post: DanbooruPost):
        return any(t in self for t in post.tags)


# endregion
