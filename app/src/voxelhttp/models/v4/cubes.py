from typing import (
    Annotated,
    Literal,
)
from pydantic import (
    Field,
    ConfigDict,
    BaseModel,
    AwareDatetime,
    field_serializer,
)
from ..generics import (
    IntGreaterEqualsZero,
    BaseResponse,
    Nickname,
)



class CubeTransaction (BaseModel):
    transacted: Annotated[AwareDatetime, Field(strict=False)]
    user_id: Nickname
    cube_count: IntGreaterEqualsZero

    model_config = ConfigDict(
        extra='forbid',
        strict=True,
    )

    @field_serializer('transacted')
    def serialize_transacted (self, value: AwareDatetime) -> str:
        return value.isoformat(timespec='milliseconds').replace('+00:00', 'Z')


class CubeResponse (BaseResponse):
    succeed: Literal[True]
    transactions: Annotated[list[CubeTransaction], Field(default_factory=list)]


class CubeTodayRankResponse (CubeResponse):
    pass


class CubeDailyRankResponse (CubeResponse):
    pass


class CubeHistoryResponse (CubeResponse):
    pass
