from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
)
from .configs import (
    _get_settings,
)
from .database import (
    setup_database,
)
from .routes import (
    setup_routes,
)



@asynccontextmanager # type: ignore
async def lifespan (app: FastAPI):
    setup_database(app, _get_settings())
    yield


app = FastAPI(lifespan=lifespan)
setup_routes(app)
