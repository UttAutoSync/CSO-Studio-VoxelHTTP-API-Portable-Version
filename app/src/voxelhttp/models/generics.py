from typing import (
    TypeVar,
    Generic,
    Annotated,
    Optional,
    Literal,
)
from typing_extensions import (
    TypedDict,
    Required,
)
from pydantic import (
    Field,
    StringConstraints,
    AfterValidator,
    ConfigDict,
    BaseModel,
)



LiteralOneOrZero = Literal[0, 1]
IntGreaterEqualsZero = Annotated[int, Field(ge=0)]
EmptyString = Annotated[str, StringConstraints(
                strip_whitespace=True,
                max_length=0,
            )]


VoxelID = Annotated[str, StringConstraints(
            pattern=r'^[0-9]{20}$',
            strip_whitespace=True,
        )]
VoxelSlotID = Annotated[VoxelID, Field(validation_alias='slot_id')]
VoxelMapID = VoxelID
VoxelImageID = VoxelID | EmptyString
VoxelMaxPlayer = Annotated[int, Field(ge=1,le=32)]
VoxelGameMode = IntGreaterEqualsZero
VoxelHasLuaScript = LiteralOneOrZero


NicknameASCII = Annotated[str, StringConstraints(
                    pattern=r'^[A-Za-z0-9\[\]]+$',
                    strip_whitespace=True,
                    min_length=4,
                    max_length=16,
                    ascii_only=True,
                )]

def nickname_bytes_checker_factory (encoding: str):
    def _func (value: str) -> str:
        if not value.isalnum():
            # Game master nicknames
            nosquares = value.strip('[]')
            if not nosquares.isalnum():
                raise ValueError('String is not an alphanumeric')
        size = len(value.encode(encoding))
        if size < 4:
            raise ValueError(f'Expected longer than 4 bytes, got {size:d} bytes')
        if size > 16:
            raise ValueError(f'Expected shorter than 16 bytes, got {size:d} bytes')
        return value
    return _func

NicknameUTF8 = Annotated[str, StringConstraints(
                strip_whitespace=True,
                ascii_only=False,
            ), AfterValidator(nickname_bytes_checker_factory('utf-8'))]

NicknameCP950 = Annotated[str, StringConstraints(
                strip_whitespace=True,
                ascii_only=False,
            ), AfterValidator(nickname_bytes_checker_factory('cp950'))]

NicknameCP949 = Annotated[str, StringConstraints(
                strip_whitespace=True,
                ascii_only=False,
            ), AfterValidator(nickname_bytes_checker_factory('cp949'))]

NicknameGB2312 = Annotated[str, StringConstraints(
                strip_whitespace=True,
                ascii_only=False,
            ), AfterValidator(nickname_bytes_checker_factory('gb2312'))]

Nickname = (
    NicknameASCII |
    NicknameCP949 |
    NicknameGB2312 |
    NicknameCP950 |
    NicknameUTF8
)


class Empty (BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        strict=True,
    )


class BaseResponse (BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        strict=True,
    )

_T = TypeVar('_T')
class Response (BaseResponse, Generic[_T]):
    succeed: Literal[True]
    result: Annotated[Optional[_T], Field(default=None, exclude_if=lambda v: v is None)]


class ErrorResult (TypedDict):
    reason: Required[str]

class ErrorResponse (BaseResponse):
    succeed: Literal[False]
    result: ErrorResult


class BaseSlot (BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        strict=True,
        validate_by_name=True,
    )


class BaseSlotList (BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        strict=True,
    )
