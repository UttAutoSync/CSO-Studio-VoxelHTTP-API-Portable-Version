from .....models.v5 import (
    SlotListBestResponse,
)
from .....models.v5 import (
    Slot,
)
from .....models.databases.slots import (
    SLOT_FIELDS_EXCLUDED,
    filter_slots_by_url_queries,
    get_best_slots as _get_slots,
)
from ..._common import (
    router,
)
from ....generics import (
    QUERY_LIMIT,
    QUERY_OFFSET,
)
from .....database import (
    SessionDep,
)



@router.get('/slots/list/best', response_model=SlotListBestResponse)
async def get_best_slots (
    session: SessionDep,
    limit: QUERY_LIMIT=10,
    offset: QUERY_OFFSET=0
):
    result: list[Slot] = []
    sqlquery = _get_slots()
    sqlquery = filter_slots_by_url_queries(sqlquery, limit, offset)
    rows = session.exec(sqlquery).all()
    if rows:
        result.extend(
            Slot.model_validate(row.model_dump(exclude=SLOT_FIELDS_EXCLUDED), by_alias=True)
            for row
            in rows
        )
    return SlotListBestResponse(succeed=True, result=result)
