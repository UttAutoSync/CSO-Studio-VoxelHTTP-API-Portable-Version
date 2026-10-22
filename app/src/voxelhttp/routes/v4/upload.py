from typing import (
    Annotated,
)
from fastapi import (
    Form,
    File,
    UploadFile,
)
from pydantic import (
    BeforeValidator,
)
from ...models.generics import (
    VoxelID,
    VoxelMaxPlayer,
    VoxelGameMode,
    VoxelHasLuaScript,
)
from ...models.v4 import (
    UploadResourcesResponse,
    UploadImagesResponse,
)
from ._common import (
    router,
)



SandboxScriptParam = Annotated[VoxelHasLuaScript, BeforeValidator(int)]


@router.post('/upload/resources/{map_id}', response_model=UploadResourcesResponse)
async def upload_map (
    map_id: VoxelID,
    slotID: Annotated[VoxelID, Form()],
    mode: Annotated[VoxelGameMode, Form()],
    max_player: Annotated[VoxelMaxPlayer, Form()],
    sandbox_script: Annotated[SandboxScriptParam, Form()],
    nexonsn: Annotated[str, Form()],
    resource: Annotated[UploadFile, File()]
):
    raise NotImplementedError()
    #buffer = await resource.read()
    #return {
    #    'succeed': True,
    #    'result': dict(),
    #}


@router.post('/upload/images/{image_id}', response_model=UploadImagesResponse)
async def upload_image (
    image_id: VoxelID,
    nexonsn: Annotated[str, Form()],
    image: Annotated[UploadFile, File()]
):
    raise NotImplementedError()
    #buffer = await image.read()
    #return {
    #    'succeed': True,
    #    'result': dict(),
    #}
