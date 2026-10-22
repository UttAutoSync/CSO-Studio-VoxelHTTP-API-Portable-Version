import json
from typing import (
    Any,
    Callable,
)
from collections.abc import (
    Awaitable,
)
from fastapi import (
    FastAPI,
    Request,
)
from fastapi.responses import (
    Response,
    JSONResponse,
)
from fastapi.exceptions import (
    RequestValidationError,
)
from ..models import (
    ErrorResponse,
)



def create_exception_handler (
    status_code: int=500,
    formatter: Callable[[Request, Exception], Any] | None = None
) -> Callable[[Request, Exception], Awaitable[Response|JSONResponse]]:
    async def _handler (request: Request, exc: Exception) -> Response|JSONResponse:
        if request.method == 'HEAD':
            return Response(status_code=status_code)
        msg = (
            formatter(request, exc)
            if formatter is not None
            else exc
        )
        error = ErrorResponse(
            succeed=False,
            result={
                'reason': json.dumps({type(exc).__name__: str(msg)}),
            },
        )
        return JSONResponse(
            status_code=status_code,
            content=error.model_dump(),
        )
    return _handler


def _rv_error_handle (_: Request, exc: RequestValidationError):
    errors = exc.errors()
    if errors:
        return errors[-1]
    return exc


def setup_default_error_handlers (app: FastAPI):
    app.add_exception_handler(RequestValidationError, create_exception_handler(422, _rv_error_handle)) # type: ignore
    app.add_exception_handler(NotImplementedError, create_exception_handler(501))
    app.add_exception_handler(Exception, create_exception_handler(500))
