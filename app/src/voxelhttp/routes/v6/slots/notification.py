from typing import (
    Annotated,
)
from fastapi import (
    Form,
)
from ....models.v6 import (
    SlotNotificationCountResponse,
    SlotNotificationDateResponse,
    SlotNotificationLikeResponse,
)
from ...generics import (
    QUERY_LIMIT,
    QUERY_OFFSET,
)
from .._common import (
    router,
)



QUERY_NSN = Annotated[str, Form()]


@router.post('/slots/notification/count', response_model=SlotNotificationCountResponse)
async def check_user_notifications_count (
    nexonsn: QUERY_NSN
):
    raise NotImplementedError()
    #return {
    #    'succeed': True,
    #    'result': 1337,
    #}


@router.post('/slots/notification/date', response_model=SlotNotificationDateResponse)
async def check_user_notifications_by_date (
    nexonsn: QUERY_NSN,
    limit: QUERY_LIMIT=10,
    offset: QUERY_OFFSET=0
):
    raise NotImplementedError()
    #return {
    #    'succeed': True,
    #    'result': [],
    #}


@router.post('/slots/notification/like', response_model=SlotNotificationLikeResponse)
async def check_user_notifications_by_like (
    nexonsn: QUERY_NSN,
    limit: QUERY_LIMIT=10,
    offset: QUERY_OFFSET=0
):
    raise NotImplementedError()
    #return {
    #    'succeed': True,
    #    'result': [],
    #}
