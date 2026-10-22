from typing import (
    Annotated,
    Literal,
    Optional,
)
from datetime import (
    datetime,
)
from pydantic import (
    Field,
    StringConstraints,
    field_serializer,
)
from ..generics import (
    LiteralOneOrZero,
    IntGreaterEqualsZero,
    EmptyString,
    VoxelID,
    VoxelSlotID,
    VoxelMapID,
    VoxelImageID,
    VoxelMaxPlayer,
    VoxelGameMode,
    VoxelHasLuaScript,
    Nickname,
    Empty,
    Response,
    BaseSlot,
    BaseSlotList,
)



VoxelParentID = (
    VoxelID |
    EmptyString |
    Annotated[str, StringConstraints(
        pattern=r'^management$',
        strip_whitespace=True,
    )]
)
VoxelPermission = IntGreaterEqualsZero
VoxelCategory = IntGreaterEqualsZero
VoxelNoticeType = IntGreaterEqualsZero


class Slot (BaseSlot):
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
    notice_type: VoxelNoticeType
    sandbox_script: VoxelHasLuaScript
    permission: VoxelPermission
    savegroup_id: str
    is_event: LiteralOneOrZero


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
    cheering_king: Optional[Nickname]
    is_event: LiteralOneOrZero


class SlotHistory (BaseSlot):
    creator_nickname: Nickname
    permission: VoxelPermission
    created: Annotated[datetime, Field(strict=False)]

    @field_serializer('created')
    def serialize_created (self, value: datetime) -> str:
        return value.isoformat(timespec='seconds').replace('T', ' ')


class SlotTemplate (BaseSlot):
    id: VoxelSlotID
    title: str
    resource_mode: VoxelGameMode
    resource_id: VoxelMapID
    resource_max_player: VoxelMaxPlayer
    description: str
    image_id: VoxelImageID
    creator_nickname: Nickname


class SlotLobby (BaseSlot):
    id: VoxelSlotID
    title: str
    resource_mode: VoxelGameMode
    resource_max_player: VoxelMaxPlayer
    image_id: VoxelImageID
    creator_nickname: Nickname
    notice_type: VoxelNoticeType
    is_event: LiteralOneOrZero


class SlotEvent (BaseSlot):
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
    notice_type: VoxelNoticeType
    sandbox_script: VoxelHasLuaScript
    savegroup_id: str
    is_event: Literal[1]


class SlotListAll (BaseSlotList):
    dev_team: list[Slot]
    best_creator: list[Slot]
    single_play: list[Slot]
    recommend: list[Slot]
    published: list[Slot]
    events: list[SlotEvent]


class SlotDetailResponse (Response[SlotDetail]):
    pass


class SlotHistoryResponse (Response[list[SlotHistory]]):
    pass


class SlotTemplateResponse (Response[list[SlotTemplate]]):
    pass


class SlotLobbyResponse (Response[SlotLobby]):
    pass


class SlotListEventResponse (Response[list[SlotEvent]]):
    pass


class SlotListAllResponse (Response[SlotListAll]):
    pass


class SlotNewbieResponse (Response[Slot]):
    pass


class SlotSimpleResponse (Response[list[Slot|Empty]]):
    pass


class SlotListResponse (Response[list[Slot]]):
    pass


class SlotListSearchResponse (SlotListResponse):
    pass


class SlotListNickResponse (SlotListResponse):
    pass


class SlotListRecommendResponse (SlotListResponse):
    pass


class SlotListBestResponse (SlotListResponse):
    pass


class SlotListDevResponse (SlotListResponse):
    pass


class SlotListPopularResponse (SlotListResponse):
    pass


class SlotListPublishResponse (SlotListResponse):
    pass


class SlotListSingleResponse (SlotListResponse):
    pass
