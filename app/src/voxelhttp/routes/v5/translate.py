from typing import (
    Annotated,
)
from fastapi import (
    Form,
    File,
    UploadFile,
)
from sqlmodel import(
    select,
    asc,
)
from ...models.generics import (
    VoxelID,
    Nickname,
)
from ...models.v5 import (
    TranslateId,
    TranslateIdResponse,
    Translate,
    TranslateListResponse,
    TranslateUploadResponse,
)
from ...models.databases.translates import (
    TableSlotTranslateV1,
    TableSlotTranslateV2,
)
from ._common import (
    router,
)
from ...database import (
    SessionDep,
)



@router.get('/translate/id/{slot_id}', response_model=TranslateIdResponse)
async def get_slot_translation_url (
    session: SessionDep,
    slot_id: VoxelID
):
    result = None
    row = session.get(TableSlotTranslateV1, slot_id)
    if row:
        buf = row.model_dump(exclude=set([
            'slot_id',
        ]))
        result = TranslateId.model_validate(buf, by_alias=True)
    return TranslateIdResponse(succeed=True, result=result)


@router.get('/translate/list/{slot_id}', response_model=TranslateListResponse)
async def get_slot_translations (
    session: SessionDep,
    slot_id: VoxelID
):
    result = None
    rows = session.exec(
        select(TableSlotTranslateV2)
        .where(
            TableSlotTranslateV2.slot_id == slot_id,
        )
        .order_by(
            asc(TableSlotTranslateV2.id),
        )
    ).all()
    if rows:
        result = [
            Translate.model_validate(row.model_dump(exclude=set([
                'id',
                'slot_id',
            ])))
            for row
            in rows
        ]
    return TranslateListResponse(succeed=True, result=result)


@router.post('/translate/upload', response_model=TranslateUploadResponse)
async def upload_translation (
    slot_id: Annotated[VoxelID, Form()],
    nickname: Annotated[Nickname, Form()],
    lang_code: Annotated[str, Form()],
    nexonsn: Annotated[str, Form()],
    translate: Annotated[UploadFile, File()]
):
    raise NotImplementedError()
    #buffer = await translate.read()
    #return {
    #    'succeed': True,
    #    'result': {},
    #}
