from contextlib import AbstractAsyncContextManager

AbstractUnitOfWork = AbstractAsyncContextManager


class FakeUOW(AbstractUnitOfWork):
    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc_value, traceback):
        ...
