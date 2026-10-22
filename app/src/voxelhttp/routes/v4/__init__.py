from ._common import (
    router,
)
from .ping import (
    ping as endpoint_ping,
    Hping as endpoint_Hping,
)
from .upload import (
    upload_map as endpoint_upload_map,
    upload_image as endpoint_upload_image,
)
from .cubes import (
    get_slot_cube_rank_today as endpoint_get_slot_cube_rank_today,
    get_slot_cube_rank_daily as endpoint_get_slot_cube_rank_daily,
    get_slot_cube_history as endpoint_get_slot_cube_history,
)
