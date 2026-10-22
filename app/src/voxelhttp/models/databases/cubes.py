from sqlmodel import (
    SQLModel,
    Field,
)



# ----------
#     V4
# ----------

class TableSlotCube (SQLModel, table=True):
    __tablename__ = 'slot_cube'

    id: int = Field(primary_key=True)
    slot_id: str = Field(foreign_key='slot.slot_id', index=True)
    transacted: str = Field(index=True)
    user_id: str = Field(index=True)
    cube_count: int


class TableSlotCubeRankDaily (SQLModel, table=True):
    __tablename__ = 'slot_cube_rank_daily'

    slot_id: str = Field(primary_key=True, foreign_key='slot.slot_id')
    transacted: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    cube_count: int


class TableSlotPoint (SQLModel, table=True):
    __tablename__ = 'slot_point'

    id: int = Field(primary_key=True)
    slot_id: str = Field(foreign_key='slot.slot_id', index=True)
    transacted: str = Field(index=True)
    user_id: str = Field(index=True)
    point_count: int


# ----------
#     V6
# ----------

class TableSlotCheer (SQLModel, table=True):
    __tablename__ = 'slot_cheer'

    slot_id: str = Field(primary_key=True, foreign_key='slot.slot_id')
    nicknames: str
