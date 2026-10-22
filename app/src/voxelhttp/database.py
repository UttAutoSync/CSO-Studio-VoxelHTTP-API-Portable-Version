from typing import (
    Annotated,
)
from sqlmodel import (
    SQLModel,
    Session,
    create_engine,
)
from sqlalchemy import (
    Engine,
    event,
)
from fastapi import (
    FastAPI,
    Depends,
)
from .configs import (
    Settings,
)



ENGINE: Engine = None


def _get_session ():
    with Session(ENGINE) as session:
        yield session

SessionDep = Annotated[Session, Depends(_get_session)]


def setup_database (_: FastAPI, configs: Settings):
    global ENGINE
    ENGINE = create_engine(configs.voxelhttp_database_url, connect_args={
        'check_same_thread': False,
    })
    if ENGINE.dialect.name == 'sqlite':
        @event.listens_for(ENGINE, 'connect')
        def _enable_foreign_keys(engineapi, _):
            engineapi.execute('PRAGMA foreign_keys=ON')

    SQLModel.metadata.create_all(ENGINE)
    return ENGINE
