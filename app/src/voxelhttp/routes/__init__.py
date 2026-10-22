from fastapi import (
    FastAPI as _FastAPI,
)
from .v4 import router as v4_router
from .v5 import router as v5_router
from .v6 import router as v6_router
from .errors import setup_default_error_handlers



def setup_routes (app: _FastAPI):
    setup_default_error_handlers(app)
    app.include_router(v4_router)
    app.include_router(v5_router)
    app.include_router(v6_router)
