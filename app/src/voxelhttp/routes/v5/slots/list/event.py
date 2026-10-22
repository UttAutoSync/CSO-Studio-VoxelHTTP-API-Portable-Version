from .....models.v5 import (
    SlotListEventResponse,
)
from .....models.v5 import (
    SlotEvent,
)
from .....models.databases.slots import (
    SLOT_EVENT_FIELDS_EXCLUDED,
    filter_slots_by_url_queries,
    get_event_slots as _get_slots,
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



@router.get('/slots/list/event', response_model=SlotListEventResponse)
async def get_event_slots (
    session: SessionDep,
    limit: QUERY_LIMIT=10,
    offset: QUERY_OFFSET=0
):
    result: list[SlotEvent] = []
    sqlquery = _get_slots()
    sqlquery = filter_slots_by_url_queries(sqlquery, limit, offset)
    rows = session.exec(sqlquery).all()
    if rows:
        result.extend(
            SlotEvent.model_validate(row.model_dump(exclude=SLOT_EVENT_FIELDS_EXCLUDED), by_alias=True)
            for row
            in rows
        )
    return SlotListEventResponse(succeed=True, result=result)
