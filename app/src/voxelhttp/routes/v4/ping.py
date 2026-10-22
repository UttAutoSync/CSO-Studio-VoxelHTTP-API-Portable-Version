from fastapi.responses import (
    Response,
    PlainTextResponse,
)
from ._common import (
    router,
)



@router.get('/ping', response_class=PlainTextResponse)
async def ping ():
    return 'cso'


# HACK: FastAPI (or Starlette) disallow HEAD method on GET routers.
#       Remove this when it got fixed.
@router.head('/ping')
async def Hping ():
    return Response(status_code=200)
