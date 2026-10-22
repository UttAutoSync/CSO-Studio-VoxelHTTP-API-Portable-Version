from datetime import (
    datetime,
    timezone,
    timedelta,
)
from sqlmodel import(
    select,
    asc,
    desc,
)
from ...models.generics import (
    VoxelID,
)
from ...models.v4 import (
    CubeTransaction,
    CubeTodayRankResponse,
    CubeDailyRankResponse,
    CubeHistoryResponse,
)
from ...models.databases.cubes import (
    TableSlotCube,
    TableSlotPoint,
    TableSlotCubeRankDaily,
)
from ._common import (
    router,
)
from ...database import (
    SessionDep,
)



@router.get('/cubes/{slot_id}/today-rank', response_model=CubeTodayRankResponse)
async def get_slot_cube_rank_today (
    session: SessionDep,
    slot_id: VoxelID
):
    result: list[CubeTransaction] = []
    start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    rows = session.exec(
        select(
            TableSlotCubeRankDaily.transacted,
            TableSlotCubeRankDaily.user_id,
            TableSlotCubeRankDaily.cube_count,
        )
        .where(
            TableSlotCubeRankDaily.slot_id == slot_id,
            TableSlotCubeRankDaily.transacted >= start.isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            TableSlotCubeRankDaily.transacted < end.isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
        )
        .order_by(
            desc(TableSlotCubeRankDaily.transacted),
            desc(TableSlotCubeRankDaily.cube_count,),
        )
    ).all()
    if rows:
        result.extend(
            CubeTransaction(
                transacted=x.transacted,
                user_id=x.user_id,
                cube_count=x.cube_count,
            )
            for x
            in rows
        )
    return CubeTodayRankResponse(succeed=True, transactions=result)


@router.get('/cubes/{slot_id}/history/{page}', response_model=CubeHistoryResponse)
async def get_slot_cube_history (
    session: SessionDep,
    slot_id: VoxelID,
    page: int
):
    result: list[CubeTransaction] = []

    sqlquery = None
    match page:
        case 1:
            sqlquery = (
                select(
                    TableSlotCube.transacted,
                    TableSlotCube.user_id,
                    TableSlotCube.cube_count,
                )
                .where(
                    TableSlotCube.slot_id == slot_id,
                )
                .order_by(
                    asc(TableSlotCube.id),
                )
            )
        case 2:
            sqlquery = (
                select(
                    TableSlotPoint.transacted,
                    TableSlotPoint.user_id,
                    TableSlotPoint.point_count.label('cube_count'),
                )
                .where(
                    TableSlotPoint.slot_id == slot_id,
                )
                .order_by(
                    asc(TableSlotPoint.id),
                )
            )

    if sqlquery is not None:
        rows = session.exec(sqlquery).all()
        if rows:
            result.extend(
                CubeTransaction(
                    transacted=x.transacted,
                    user_id=x.user_id,
                    cube_count=x.cube_count,
                )
                for x
                in rows
            )

    return CubeHistoryResponse(succeed=True, transactions=result)


@router.get('/cubes/{slot_id}/daily-rank', response_model=CubeDailyRankResponse)
async def get_slot_cube_rank_daily (
    session: SessionDep,
    slot_id: VoxelID
):
    result: list[CubeTransaction] = []
    rows = session.exec(
        select(
            TableSlotCubeRankDaily.transacted,
            TableSlotCubeRankDaily.user_id,
            TableSlotCubeRankDaily.cube_count,
        )
        .where(
            TableSlotCubeRankDaily.slot_id == slot_id,
        )
        .order_by(
            desc(TableSlotCubeRankDaily.transacted),
        )
    ).all()
    if rows:
        result.extend(
            CubeTransaction(
                transacted=x.transacted,
                user_id=x.user_id,
                cube_count=x.cube_count,
            )
            for x
            in rows
        )
    return CubeDailyRankResponse(succeed=True, transactions=result)
