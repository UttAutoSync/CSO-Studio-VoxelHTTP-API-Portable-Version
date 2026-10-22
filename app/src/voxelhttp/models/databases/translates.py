from sqlmodel import (
    SQLModel,
    Field,
    Index,
    text,
)



class TableSlotTranslateV1 (SQLModel, table=True):
    __tablename__ = 'slot_translate_v1'

    slot_id: str = Field(primary_key=True, foreign_key='slot.slot_id')
    translate_url: str


class TableSlotTranslateV2 (SQLModel, table=True):
    __tablename__ = 'slot_translate_v2'

    id: int = Field(primary_key=True)
    slot_id: str = Field(foreign_key='slot.slot_id', index=True)
    nickname: str = Field(index=True)
    lang_code: str = Field(index=True)
    view_count: int = Field(default=0)
    translate_id: str = Field(index=True)
    created: str
    is_default: int = Field(default=1)
    translate_url: str

    __table_args__ = (
        Index(
            'idx_slot_translate_v2_unique_one_default',
            'slot_id',
            unique=True,
            sqlite_where=text('is_default = 1'),
        ),
    )
