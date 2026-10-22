from typing import (
    Annotated,
)
from fastapi import (
    Query,
)
from sqlmodel import (
    select,
)
from ....models.v5 import (
    Slot,
    SlotSimpleResponse,
)
from ....models.databases.slots import (
    SLOT_FIELDS_EXCLUDED,
    TableSlot,
)
from ....models.generics import (
    Empty,
)
from .._common import (
    router,
)
from ....database import (
    SessionDep,
)



@router.get('/slots/simple', response_model=SlotSimpleResponse)
async def get_slots_by_ids (
    session: SessionDep,
    ids: Annotated[str, Query()]
):
    result: list[Slot|Empty] = []
    if ids:
        slot_ids = ids.split(',')
        rows = session.exec(
            select(TableSlot)
            .where(
                TableSlot.slot_id.in_(slot_ids)
            )
        ).all()
        slots = {
            row.slot_id: row
            for row
            in rows
        }
        result.extend(
            Slot.model_validate(
                slots[k].model_dump(exclude=SLOT_FIELDS_EXCLUDED),
                by_alias=True,
            )
            if k in slots
            else Empty()
            for k
            in slot_ids
        )
    return SlotSimpleResponse(succeed=True, result=result)
