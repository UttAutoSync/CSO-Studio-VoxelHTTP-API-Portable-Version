from typing import (
    Annotated,
    Literal,
    Optional,
)
from pydantic import (
    Field,
)
from ..v5.slots import (
    Slot,
    VoxelParentID,
    VoxelPermission,
    VoxelCategory,
    VoxelNoticeType,
    SlotListResponse,
)
from ..generics import (
    LiteralOneOrZero,
    IntGreaterEqualsZero,
    VoxelSlotID,
    VoxelMapID,
    VoxelImageID,
    VoxelMaxPlayer,
    VoxelGameMode,
    VoxelHasLuaScript,
    Nickname,
    BaseResponse,
    Response,
    BaseSlot,
    BaseSlotList,
)



class SlotDetail (BaseSlot):
    id: VoxelSlotID
    title: str
    resource_mode: VoxelGameMode
    resource_id: VoxelMapID
    resource_max_player: VoxelMaxPlayer
    permission: VoxelPermission
    description: str
    parents_slot_id: VoxelParentID
    image_id: VoxelImageID
    creator_nickname: Nickname
    like_count: IntGreaterEqualsZero
    play_count: IntGreaterEqualsZero
    bookmark_count: IntGreaterEqualsZero
    cube_count: IntGreaterEqualsZero
    sandbox_script: VoxelHasLuaScript
    savegroup_id: str
    slot_category: VoxelCategory
    cheering_king: Optional[Nickname]
    tags: list[str]


class SlotListSearch (Slot):
    tag_name: Annotated[
        Optional[str],
        Field(default=None, exclude_if=lambda v: v is None),
    ]


class SlotNotification (Slot):
    creator_message: str


class SlotListAllPromotion (BaseSlot):
    id: VoxelSlotID
    title: str
    resource_mode: VoxelGameMode
    resource_id: VoxelMapID
    resource_max_player: VoxelMaxPlayer
    image_id: VoxelImageID
    creator_nickname: Nickname
    like_count: IntGreaterEqualsZero
    play_count: IntGreaterEqualsZero
    cube_count: IntGreaterEqualsZero
    slot_category: VoxelCategory
    sandbox_script: VoxelHasLuaScript
    permission: VoxelPermission
    notice_type: VoxelNoticeType
    group_id: str
    is_event: LiteralOneOrZero


class SlotListAll (BaseSlotList):
    promotion: list[SlotListAllPromotion]
    events: list[Slot]
    soar_popular: list[Slot]
    dev_team: list[Slot]
    popular_rank: list[Slot]
    best_creator: list[Slot]
    single_play: list[Slot]
    published: list[Slot]
    liked: list[Slot]
    notable: list[Slot]


class SlotDetailResponse (Response[SlotDetail]):
    pass


class SlotListSearchResponse (Response[list[SlotListSearch]]):
    pass


class SlotNotificationDateResponse (Response[list[SlotNotification]]):
    pass


class SlotNotificationLikeResponse (Response[list[SlotNotification]]):
    pass


class SlotNotificationCountResponse (BaseResponse):
    succeed: Literal[True]
    result: IntGreaterEqualsZero


class SlotListAllResponse (Response[SlotListAll]):
    pass


class SlotListPromotionResponse (SlotListResponse):
    pass


class SlotListEventResponse (SlotListResponse):
    pass


class SlotListSoarRankResponse (SlotListResponse):
    pass


class SlotListDevResponse (SlotListResponse):
    pass


class SlotListRankResponse (SlotListResponse):
    pass


class SlotListBestCreatorResponse (SlotListResponse):
    pass


class SlotListSingleResponse (SlotListResponse):
    pass


class SlotListPublishedResponse (SlotListResponse):
    pass


class SlotListLikeResponse (SlotListResponse):
    pass


class SlotListNotableResponse (SlotListResponse):
    pass
