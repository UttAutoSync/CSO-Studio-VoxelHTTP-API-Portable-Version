from json import (
    loads,
)
from ...models.generics import (
    VoxelID,
)
from ...models.v6 import (
    CubeCheerResponse,
)
from ...models.databases.cubes import (
    TableSlotCheer,
)
from ._common import (
    router,
)
from ...database import (
    SessionDep,
)



@router.get('/cube/cheer/{slot_id}', response_model=CubeCheerResponse)
async def get_slot_cube_cheers (
    session: SessionDep,
    slot_id: VoxelID
):
    result = None
    row = session.get(TableSlotCheer, slot_id)
    if row:
        result = loads(row.nicknames)
    return CubeCheerResponse(succeed=True, result=result)
