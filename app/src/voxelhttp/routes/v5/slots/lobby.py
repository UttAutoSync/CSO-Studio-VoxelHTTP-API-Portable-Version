from sqlmodel import (
    select,
    desc,
)
from ....models.v5 import (
    SlotLobby,
    SlotLobbyResponse,
)
from ....models.databases.slots import (
    SLOT_LOBBY_FIELDS_EXCLUDED,
    TableSlot,
    exclude_template_slots,
)
from .._common import (
    router,
)
from ....database import (
    SessionDep,
)



@router.get('/slots/lobby_menu_ex', response_model=SlotLobbyResponse)
async def get_lobby_slot (
    session: SessionDep
):
    result: SlotLobby|None = None
    sqlquery = (
        select(TableSlot)
        .order_by(
            desc(TableSlot.notice_type),
            desc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    row = session.exec(sqlquery).first()
    if row:
        result = SlotLobby.model_validate(row.model_dump(exclude=SLOT_LOBBY_FIELDS_EXCLUDED), by_alias=True)
    return SlotLobbyResponse(succeed=True, result=result)
