from contextlib import AbstractAsyncContextManager
from typing import Protocol


class AbstractUOW(Protocol):
    async def commit(self, *args, **kwargs):
        ...


AbstractUOWFabric = AbstractAsyncContextManager[AbstractUOW]
