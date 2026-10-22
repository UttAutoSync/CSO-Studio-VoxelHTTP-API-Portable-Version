from .....models.v6 import (
    SlotListAllResponse,
    SlotListAll,
    SlotListAllPromotion,
)
from .....models.v5 import (
    Slot,
)
from .....models.databases.slots import (
    SLOT_FIELDS_EXCLUDED,
    SLOT_PROMOTION_FIELDS_EXCLUDED,
    filter_slots_by_url_queries,
    get_promoted_slots,
    get_event_slots,
    get_average_slots,
    get_developer_slots,
    get_ranked_slots,
    #get_best_slots,
    get_singleplayer_slots,
    get_new_slots,
    get_liked_slots,
)
from ..._common import (
    router,
)
from .....database import (
    SessionDep,
)



SLOT_LIST_ALL_MAPPING = {
    'promotion': (get_promoted_slots, SlotListAllPromotion, SLOT_PROMOTION_FIELDS_EXCLUDED),
    'events': (get_event_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'soar_popular': (lambda: get_average_slots(is_above=True), Slot, SLOT_FIELDS_EXCLUDED),
    'dev_team': (get_developer_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'popular_rank': (get_ranked_slots, Slot, SLOT_FIELDS_EXCLUDED),
    #'best_creator': (get_best_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'single_play': (get_singleplayer_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'published': (get_new_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'liked': (get_liked_slots, Slot, SLOT_FIELDS_EXCLUDED),
    'notable': (lambda: get_average_slots(is_above=False), Slot, SLOT_FIELDS_EXCLUDED),
}


@router.get('/slots/list/all', response_model=SlotListAllResponse)
async def get_all_slots (
    session: SessionDep
):
    result: dict[str, list] = {}
    result.setdefault('best_creator', [])
    for k, props in SLOT_LIST_ALL_MAPPING.items():
        target = result.setdefault(k, [])
        is_promotion = (k == 'promotion')
        getter, model, excludes = props
        sqlquery = getter()
        limit = 12
        if is_promotion:
            limit = 3
        sqlquery = filter_slots_by_url_queries(sqlquery, limit, 0)
        rows = session.exec(sqlquery).all()
        if rows:
            if is_promotion:
                target.extend(
                    model.model_validate({
                        **row.model_dump(exclude=excludes),
                        'group_id': '',
                    }, by_alias=True)
                    for row
                    in rows
                )
            else:
                target.extend(
                    model.model_validate(row.model_dump(exclude=excludes), by_alias=True)
                    for row
                    in rows
                )
    result = SlotListAll.model_validate(result, by_alias=True)
    return SlotListAllResponse(succeed=True, result=result)
