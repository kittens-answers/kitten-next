from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from answers.entrypoints.api.exc_handlers import config_exc_handlers
from answers.entrypoints.api.routers import config_routes


def get_app(lifespan):
    app = FastAPI(lifespan=lifespan)
    config_routes(app)
    config_exc_handlers(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
