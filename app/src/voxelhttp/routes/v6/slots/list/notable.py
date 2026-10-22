from .....models.v6 import (
    SlotListNotableResponse,
)
from .....models.v5 import (
    Slot,
)
from .....models.databases.slots import (
    SLOT_FIELDS_EXCLUDED,
    v6_filter_slots_by_url_queries,
    get_average_slots as _get_slots,
)
from ..._common import (
    router,
)
from ....generics import (
    QUERY_LIMIT,
    QUERY_OFFSET,
    QUERY_MODE,
)
from .....database import (
    SessionDep,
)



@router.get('/slots/list/notable', response_model=SlotListNotableResponse)
async def get_below_average_slots (
    session: SessionDep,
    limit: QUERY_LIMIT=10,
    offset: QUERY_OFFSET=0,
    mode: QUERY_MODE=None
):
    result: list[Slot] = []
    sqlquery = _get_slots(is_above=False)
    sqlquery = v6_filter_slots_by_url_queries(sqlquery, limit, offset, mode)
    rows = session.exec(sqlquery).all()
    if rows:
        result.extend(
            Slot.model_validate(row.model_dump(exclude=SLOT_FIELDS_EXCLUDED), by_alias=True)
            for row
            in rows
        )
    return SlotListNotableResponse(succeed=True, result=result)
