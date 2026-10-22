from ._common import (
    router,
)
from .statistics import (
    create_statistics as endpoint_create_statistics,
)
from .translate import (
    get_slot_translation_url as endpoint_get_slot_translation_url,
    get_slot_translations as endpoint_get_slot_translations,
    upload_translation as endpoint_upload_translation,
)
from .slots import *
