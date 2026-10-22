from typing import (
    Annotated,
)
from fastapi import (
    Form,
)
from ...models.generics import (
    IntGreaterEqualsZero,
    VoxelID,
)
from ...models.v5 import (
    StatisticsCreateResponse,
)
from ._common import (
    router,
)



@router.post('/statistics/create/{slot_id}', response_model=StatisticsCreateResponse)
async def create_statistics (
    slot_id: VoxelID,
    nexonsn: Annotated[str, Form()],
    block_change_count: Annotated[IntGreaterEqualsZero, Form()],
    trigger_change_count: Annotated[IntGreaterEqualsZero, Form()],
    trigger_prop_change_count: Annotated[IntGreaterEqualsZero, Form()],
    lua_change_count: Annotated[IntGreaterEqualsZero, Form()],
    create_time: Annotated[IntGreaterEqualsZero, Form()]
):
    raise NotImplementedError()
    #return {
    #    'succeed': True,
    #    'result': dict(),
    #}
