from sqlmodel import (
    select,
)
from .....models.v5 import (
    SlotTemplate,
    SlotTemplateResponse,
)
from .....models.databases.slots import (
    SLOT_TEMPLATE_FIELDS_EXCLUDED,
    TableSlot,
    TableSlotListTemplate,
)
from ..._common import (
    router,
)
from .....database import (
    SessionDep,
)



@router.get('/slots/list/template', response_model=SlotTemplateResponse)
async def get_template_slots (session: SessionDep):
    result: list[SlotTemplate] = []
    rows = session.exec(
        select(TableSlot)
        .join(
            TableSlotListTemplate,
            TableSlotListTemplate.slot_id == TableSlot.slot_id,
        )
    ).all()
    if rows:
        result.extend(
            SlotTemplate.model_validate(row.model_dump(exclude=SLOT_TEMPLATE_FIELDS_EXCLUDED), by_alias=True)
            for row
            in rows
        )
    return SlotTemplateResponse(succeed=True, result=result)
