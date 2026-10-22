from .....models.v5 import (
    SlotListAllResponse,
)
from .....models.v5 import (
    SlotListAll,
    Slot,
    SlotEvent,
)
from .....models.databases.slots import (
    SLOT_FIELDS_EXCLUDED,
    SLOT_EVENT_FIELDS_EXCLUDED,
    filter_slots_by_url_queries,
    get_developer_slots,
    get_best_slots,
    get_singleplayer_slots,
    get_recommended_slots,
    get_new_slots,
    get_event_slots,
)
from ..._common import (
    router,
)
from .....database import (
    SessionDep,
)



SLOT_LIST_ALL_MAPPING = {
    'dev_team': (get_developer_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'best_creator': (get_best_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'single_play': (get_singleplayer_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'recommend': (get_recommended_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'published': (get_new_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'events': (get_event_slots, SlotEvent, SLOT_EVENT_FIELDS_EXCLUDED),
}


@router.get('/slots/list/all', response_model=SlotListAllResponse)
async def get_all_slots (
    session: SessionDep
):
    result: dict[str, list] = {}
    for k, props in SLOT_LIST_ALL_MAPPING.items():
        target = result.setdefault(k, [])
        getter, model, excludes = props
        sqlquery = getter()
        sqlquery = filter_slots_by_url_queries(sqlquery, 15, 0)
        rows = session.exec(sqlquery).all()
        if rows:
            target.extend(
                model.model_validate(row.model_dump(exclude=excludes), by_alias=True)
                for row
                in rows
            )
    result = SlotListAll.model_validate(result, by_alias=True)
    return SlotListAllResponse(succeed=True, result=result)
