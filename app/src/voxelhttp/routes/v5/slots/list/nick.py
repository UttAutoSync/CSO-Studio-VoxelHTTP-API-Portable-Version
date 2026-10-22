from sqlmodel import (
    select,
)
from .....models.v5 import (
    Slot,
    SlotListNickResponse,
)
from .....models.databases.slots import (
    SLOT_FIELDS_EXCLUDED,
    TableSlot,
    filter_slots_by_url_queries,
    exclude_template_slots,
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



@router.get('/slots/list/nick/{nickname}', response_model=SlotListNickResponse)
async def get_slots_by_nickname (
    session: SessionDep,
    nickname: str,
    limit: QUERY_LIMIT=10,
    offset: QUERY_OFFSET=0
):
    result: list[Slot] = []
    sqlquery = (
        select(TableSlot)
        .where(
            TableSlot.creator_nickname.ilike(nickname),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    sqlquery = filter_slots_by_url_queries(sqlquery, limit, offset)
    rows = session.exec(sqlquery).all()
    if rows:
        result.extend(
            Slot.model_validate(row.model_dump(exclude=SLOT_FIELDS_EXCLUDED), by_alias=True)
            for row
            in rows
        )
    return SlotListNickResponse(succeed=True, result=result)
