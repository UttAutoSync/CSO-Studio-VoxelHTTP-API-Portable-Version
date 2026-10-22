from typing import (
    Annotated,
    Optional,
)
from fastapi import (
    Query,
)



QUERY_Q         = Annotated[str, Query()]
QUERY_LIMIT     = Annotated[int, Query(gt=0, le=100)]
QUERY_OFFSET    = Annotated[int, Query(ge=0)]
QUERY_MODE      = Annotated[Optional[int], Query(ge=0)]
