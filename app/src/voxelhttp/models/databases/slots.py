from sqlmodel import (
    SQLModel,
    Field,
    select,
    or_,
    exists,
    case,
    desc,
    asc,
    func,
)
from sqlmodel.sql.expression import (
    SelectOfScalar,
)



V5_SLOT_DETAIL_FIELDS_EXCLUDED = set([
    'slot_category',
    'tags',
    'notice_type',
])
V6_SLOT_DETAIL_FIELDS_EXCLUDED = set([
    'is_event',
    'notice_type',
])
SLOT_FIELDS_EXCLUDED = set([
    'description',
    'parents_slot_id',
    'bookmark_count',
    'cheering_king',
    'tags',
])
SLOT_TEMPLATE_FIELDS_EXCLUDED = set([
    'permission',
    'parents_slot_id',
    'like_count',
    'play_count',
    'bookmark_count',
    'cube_count',
    'sandbox_script',
    'savegroup_id',
    'cheering_king',
    *V5_SLOT_DETAIL_FIELDS_EXCLUDED,
    *V6_SLOT_DETAIL_FIELDS_EXCLUDED,
])
SLOT_LOBBY_FIELDS_EXCLUDED = set([
    'resource_id',
    'permission',
    'like_count',
    'play_count',
    'cube_count',
    'sandbox_script',
    'savegroup_id',
    'slot_category',
    *SLOT_FIELDS_EXCLUDED,
])
SLOT_EVENT_FIELDS_EXCLUDED = set([
    'permission',
    *SLOT_FIELDS_EXCLUDED,
])
SLOT_PROMOTION_FIELDS_EXCLUDED =  set([
    'savegroup_id',
    *SLOT_FIELDS_EXCLUDED,
])


class TableSlot (SQLModel, table=True):
    __tablename__ = 'slot'

    slot_id: str = Field(primary_key=True)
    title: str | None = Field(default=None)
    resource_mode: int | None = Field(default=None)
    resource_id: str | None = Field(default=None, index=True)
    resource_max_player: int | None = Field(default=None)
    permission: int | None = Field(default=None)
    description: str | None = Field(default=None)
    parents_slot_id: str | None = Field(default=None, index=True)
    image_id: str | None = Field(default=None, index=True)
    creator_nickname: str | None = Field(default=None, index=True)
    like_count: int | None = Field(default=None)
    play_count: int | None = Field(default=None)
    bookmark_count: int | None = Field(default=None)
    cube_count: int | None = Field(default=None)
    sandbox_script: int | None = Field(default=None)
    savegroup_id: str | None = Field(default=None)
    slot_category: int | None = Field(default=None)
    cheering_king: str | None = Field(default=None, index=True)
    tags: str | None = Field(default=None)
    notice_type: int | None = Field(default=None)
    is_event: int | None = Field(default=None)


class TableSlotHistory (SQLModel, table=True):
    __tablename__ = 'slot_history'

    id: int | None = Field(default=None, primary_key=True)
    slot_id: str = Field(foreign_key='slot.slot_id', index=True)
    creator_nickname: str = Field(index=True)
    created: str
    permission: int


class TableSlotListTemplate (SQLModel, table=True):
    __tablename__ = 'slot_list_template'

    slot_id: str = Field(primary_key=True, foreign_key='slot.slot_id')


def filter_slots_by_url_queries (
    sqlquery: SelectOfScalar[TableSlot],
    limit: int,
    offset: int,
):
    return sqlquery.limit(limit).offset(offset * limit)


def exclude_template_slots (sqlquery: SelectOfScalar[TableSlot]):
    return sqlquery.where(
        ~exists().where(
            TableSlotListTemplate.slot_id == TableSlot.slot_id
        )
    )


def search_slots (q: str, limit: int, offset: int):
    sqlquery: SelectOfScalar[TableSlot] = select(TableSlot)
    if q:
        pattern = f'%{q}%'
        sqlquery = sqlquery.where(or_(
            TableSlot.title.ilike(pattern),
            TableSlot.creator_nickname.ilike(pattern),
        ))
    sqlquery = exclude_template_slots(sqlquery)
    sqlquery = sqlquery.order_by(TableSlot.slot_id)
    return filter_slots_by_url_queries(sqlquery, limit, offset)


def get_singleplayer_slots ():
    sqlquery = (
        select(TableSlot)
        .where(
            TableSlot.resource_max_player == 1,
        )
        .order_by(
            case(
                {
                    2: 0,
                    6: 2,
                    7: 2,
                },
                value=TableSlot.slot_category,
                else_=1,
            ),
            desc(TableSlot.slot_category),
            desc(TableSlot.like_count),
            desc(TableSlot.play_count),
            desc(TableSlot.cube_count),
            desc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    return sqlquery


def get_developer_slots ():
    sqlquery = (
        select(TableSlot)
        .where(
            TableSlot.parents_slot_id == 'management',
        )
        .order_by(
            case(
                {
                    2: 0,
                },
                value=TableSlot.slot_category,
                else_=1,
            ),
            desc(TableSlot.like_count),
            desc(TableSlot.play_count),
            desc(TableSlot.cube_count),
            desc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    return sqlquery


def get_best_slots ():
    sqlquery = (
        select(TableSlot)
        .order_by(
            desc(TableSlot.like_count),
            desc(TableSlot.play_count),
            desc(TableSlot.cube_count),
            desc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    return sqlquery


def get_recommended_slots ():
    sqlquery = (
        select(TableSlot)
        .order_by(
            desc(TableSlot.notice_type),
            case(
                {
                    2: 0,
                },
                value=TableSlot.slot_category,
                else_=1,
            ),
            desc(TableSlot.slot_category),
            desc(TableSlot.like_count),
            desc(TableSlot.play_count),
            desc(TableSlot.cube_count),
            asc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    return sqlquery


def get_new_slots ():
    sqlquery = (
        select(TableSlot)
        .order_by(
            desc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    return sqlquery


def get_event_slots ():
    sqlquery = (
        select(TableSlot)
        .where(
            TableSlot.is_event == 1,
        )
        .order_by(
            desc(TableSlot.notice_type),
            desc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    return sqlquery


def get_popular_slots ():
    sqlquery = (
        select(TableSlot)
        .order_by(
            desc(TableSlot.play_count),
            asc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    return sqlquery


def get_liked_slots ():
    sqlquery = (
        select(TableSlot)
        .order_by(
            desc(TableSlot.like_count),
            asc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    return sqlquery


def get_ranked_slots ():
    return get_popular_slots()


def get_average_subqueries ():
    return (
        select(func.avg(TableSlot.play_count)).scalar_subquery(),
        select(func.avg(TableSlot.like_count)).scalar_subquery(),
        select(func.avg(TableSlot.cube_count)).scalar_subquery(),
        select(func.avg(TableSlot.bookmark_count)).scalar_subquery(),
    )


def get_average_slots (is_above: bool=True):
    sqlquery = (
        select(TableSlot)
        .order_by(
            desc(TableSlot.like_count),
            desc(TableSlot.play_count),
            desc(TableSlot.cube_count),
            desc(TableSlot.bookmark_count),
            desc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    avg_play, avg_like, avg_cube, avg_bookmark = get_average_subqueries()
    if is_above:
        sqlquery = sqlquery.where(
            TableSlot.play_count >= avg_play,
            TableSlot.like_count >= avg_like,
            TableSlot.cube_count >= avg_cube,
        )
    else:
        sqlquery = sqlquery.where(
            TableSlot.play_count < avg_play,
            TableSlot.like_count < avg_like,
            TableSlot.cube_count < avg_cube,
        )
    return sqlquery


def get_promoted_slots ():
    sqlquery = (
        select(TableSlot)
        .order_by(
            case(
                {
                    6: 1,
                    7: 1,
                },
                value=TableSlot.slot_category,
                else_=0,
            ),
            desc(TableSlot.slot_category),
            desc(TableSlot.like_count),
            desc(TableSlot.play_count),
            desc(TableSlot.cube_count),
            desc(TableSlot.slot_id),
        )
    )
    sqlquery = exclude_template_slots(sqlquery)
    return sqlquery


# ----------
#     V6
# ----------

def v6_filter_slots_by_url_queries (
    sqlquery: SelectOfScalar[TableSlot],
    limit: int,
    offset: int,
    mode: int|None,
):
    if mode is not None:
        sqlquery = sqlquery.where(
            TableSlot.resource_mode == mode,
        )
    return filter_slots_by_url_queries(sqlquery, limit, offset)


def v6_search_slots (q: str, tags: list[str], limit: int, offset: int, mode: int|None):
    sqlquery: SelectOfScalar[TableSlot] = select(TableSlot)
    if q:
        pattern = f'%{q}%'
        sqlquery = sqlquery.where(or_(
            TableSlot.title.ilike(pattern),
            TableSlot.creator_nickname.ilike(pattern),
            TableSlot.description.ilike(pattern),
        ))
    if tags:
        pattern = '%"{tag}"%'
        sqlquery = sqlquery.where(or_(*(
            TableSlot.tags.ilike(pattern.format(tag=x))
            for x
            in tags
        )))
    sqlquery = exclude_template_slots(sqlquery)
    sqlquery = sqlquery.order_by(TableSlot.slot_id)
    return v6_filter_slots_by_url_queries(sqlquery, limit, offset, mode)
