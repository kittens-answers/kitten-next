from contextlib import asynccontextmanager

from fastapi import FastAPI

from answers.domain.bootstrap import BootStrap
from answers.entrypoints.api import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with BootStrap() as boot:
        app.state.boot = boot
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=routers.router)
