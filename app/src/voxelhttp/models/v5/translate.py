from typing import (
    Annotated,
)
from datetime import (
    date,
)
from pydantic import (
    Field,
    ConfigDict,
    BaseModel,
    HttpUrl,
)
from ..generics import (
    LiteralOneOrZero,
    IntGreaterEqualsZero,
    VoxelID,
    Nickname,
    Response,
)



VoxelTranslateID = VoxelID


class Translate (BaseModel):
    nickname: Nickname
    lang_code: str
    view_count: IntGreaterEqualsZero
    translate_id: VoxelTranslateID
    created: Annotated[date, Field(strict=False)]
    is_default: LiteralOneOrZero
    translate_url: Annotated[HttpUrl, Field(strict=False)]

    model_config = ConfigDict(
        extra='forbid',
        strict=True,
    )


class TranslateId (BaseModel):
    url: Annotated[HttpUrl, Field(validation_alias='translate_url')]

    model_config = ConfigDict(
        extra='forbid',
        strict=True,
        validate_by_name=True,
    )


class TranslateUpload (BaseModel):
    translate_id: VoxelTranslateID

    model_config = ConfigDict(
        extra='forbid',
        strict=True,
    )


class TranslateListResponse (Response[list[Translate]]):
    pass


class TranslateIdResponse (Response[TranslateId]):
    pass


class TranslateUploadResponse (Response[TranslateUpload]):
    pass
