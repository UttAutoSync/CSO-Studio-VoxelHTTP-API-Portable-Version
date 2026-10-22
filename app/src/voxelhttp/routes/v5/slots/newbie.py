from sqlmodel import (
    select,
    desc,
)
from ....models.v5 import (
    Slot,
    SlotNewbieResponse,
)
from ....models.databases.slots import (
    SLOT_FIELDS_EXCLUDED,
    TableSlot,
    exclude_template_slots,
)
from .._common import (
    router,
)
from ....database import (
    SessionDep,
)



@router.get('/slots/newbie', response_model=SlotNewbieResponse)
async def get_newbie_slot (
    session: SessionDep
):
    result: Slot|None = None
    sqlquery = (
        select(TableSlot)
        .order_by(
            desc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    row = session.exec(sqlquery).first()
    if row:
        result = Slot.model_validate(row.model_dump(exclude=SLOT_FIELDS_EXCLUDED), by_alias=True)
    return SlotNewbieResponse(succeed=True, result=result)
