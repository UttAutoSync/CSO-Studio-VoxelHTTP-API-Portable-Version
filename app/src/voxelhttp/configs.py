from typing import (
    Annotated,
)
from functools import (
    lru_cache,
)
from fastapi import (
    Depends,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)



class Settings (BaseSettings):
    voxelhttp_database_url: str = 'sqlite:///db.sqlite3'

    model_config = SettingsConfigDict(
        env_file='voxelhttp.env',
    )


@lru_cache
def _get_settings ():
    return Settings()

SettingDep = Annotated[Settings, Depends(_get_settings)]
