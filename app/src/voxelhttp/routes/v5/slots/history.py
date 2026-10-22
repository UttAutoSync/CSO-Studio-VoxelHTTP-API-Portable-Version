from sqlmodel import(
    select,
    asc,
)
from ....models.generics import (
    VoxelID,
)
from ....models.v5 import (
    SlotHistory,
    SlotHistoryResponse,
)
from ....models.databases.slots import (
    TableSlotHistory,
)
from .._common import (
    router,
)
from ....database import (
    SessionDep,
)



@router.get('/slots/history/{slot_id}', response_model=SlotHistoryResponse)
async def get_slot_history (
    session: SessionDep,
    slot_id: VoxelID
):
    result: list[SlotHistory] = []
    rows = session.exec(
        select(TableSlotHistory)
        .where(
            TableSlotHistory.slot_id == slot_id,
        )
        .order_by(
            asc(TableSlotHistory.created),
        )
    )
    if rows:
        result.extend(
            SlotHistory.model_validate(row.model_dump(exclude=set([
                'id',
                'slot_id',
            ])))
            for row
            in rows
        )
    return SlotHistoryResponse(succeed=True, result=result)
