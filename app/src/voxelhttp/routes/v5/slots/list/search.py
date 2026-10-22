from .....models.v5 import (
    Slot,
    SlotListSearchResponse,
)
from .....models.databases.slots import (
    SLOT_FIELDS_EXCLUDED,
    search_slots,
)
from ..._common import (
    router,
)
from ....generics import (
    QUERY_Q,
    QUERY_LIMIT,
    QUERY_OFFSET,
)
from .....database import (
    SessionDep,
)



@router.get('/slots/list/search', response_model=SlotListSearchResponse)
async def get_slots_by_search (
    session: SessionDep,
    q: QUERY_Q='',
    limit: QUERY_LIMIT=10,
    offset: QUERY_OFFSET=0
):
    result: list[Slot] = []
    sqlquery = search_slots(q, limit, offset)
    rows = session.exec(sqlquery).all()
    if rows:
        result.extend(
            Slot.model_validate(row.model_dump(exclude=SLOT_FIELDS_EXCLUDED), by_alias=True)
            for row
            in rows
        )
    return SlotListSearchResponse(succeed=True, result=result)
