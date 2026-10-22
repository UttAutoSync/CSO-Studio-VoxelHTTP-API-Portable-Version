from ....models.generics import (
    VoxelID,
)
from ....models.v5 import (
    SlotDetail,
    SlotDetailResponse,
)
from ....models.databases.slots import (
    V5_SLOT_DETAIL_FIELDS_EXCLUDED,
    TableSlot,
)
from .._common import (
    router,
)
from ....database import (
    SessionDep,
)



@router.get('/slots/detail/{slot_id}', response_model=SlotDetailResponse)
async def get_slot_details (
    session: SessionDep,
    slot_id: VoxelID
):
    result = None
    row = session.get(TableSlot, slot_id)
    if row:
        buf = row.model_dump(exclude=V5_SLOT_DETAIL_FIELDS_EXCLUDED)
        result = SlotDetail.model_validate(buf, by_alias=True)
    return SlotDetailResponse(succeed=True, result=result)
