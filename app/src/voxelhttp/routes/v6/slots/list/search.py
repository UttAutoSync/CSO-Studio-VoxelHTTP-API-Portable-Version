from typing import (
    Annotated,
)
from json import (
    loads,
)
from fastapi import (
    Query,
)
from .....models import (
    SlotListSearch,
)
from .....models.v6 import (
    SlotListSearchResponse,
)
from .....models.databases.slots import (
    SLOT_FIELDS_EXCLUDED,
    v6_search_slots,
)
from ....generics import (
    QUERY_Q,
    QUERY_LIMIT,
    QUERY_OFFSET,
    QUERY_MODE,
)
from ..._common import (
    router,
)
from .....database import (
    SessionDep,
)



QUERY_TAG = Annotated[str, Query()]


@router.get('/slots/list/search', response_model=SlotListSearchResponse)
async def get_slots_by_search (
    session: SessionDep,
    q: QUERY_Q='',
    tag: QUERY_TAG='',
    limit: QUERY_LIMIT=10,
    offset: QUERY_OFFSET=0,
    mode: QUERY_MODE=None
):
    result: list[SlotListSearch] = []
    tags: list[str] = []
    if tag:
        tags = tag.split(',')
    sqlquery = v6_search_slots(q, tags, limit, offset, mode)
    rows = session.exec(sqlquery).all()
    if rows:
        for row in rows:
            buf = row.model_dump(exclude=SLOT_FIELDS_EXCLUDED)
            if tags:
                row_tags = loads(row.tags)
                for query_tag in tags:
                    for row_tag in row_tags:
                        if query_tag.lower() == row_tag.lower():
                            buf['tag_name'] = row_tag
                            break
            result.append(SlotListSearch.model_validate(buf, by_alias=True))
    return SlotListSearchResponse(succeed=True, result=result)
