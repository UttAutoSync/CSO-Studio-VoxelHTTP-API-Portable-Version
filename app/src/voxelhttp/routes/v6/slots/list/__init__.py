from .search import (
    get_slots_by_search as endpoint_get_slots_by_search,
)
from .event import (
    get_event_slots as endpoint_get_event_slots,
)
from .soar_rank import (
    get_above_average_slots as endpoint_get_above_average_slots,
)
from .dev import (
    get_developer_slots as endpoint_get_developer_slots,
)
from .rank import (
    get_ranked_slots as endpoint_get_ranked_slots,
)
from .single import (
    get_singleplayer_slots as endpoint_get_singleplayer_slots,
)
from .published import (
    get_new_slots as endpoint_get_new_slots,
)
from .like import (
    get_liked_slots as endpoint_get_liked_slots,
)
from .notable import (
    get_below_average_slots as endpoint_get_below_average_slots,
)
from .all import (
    get_all_slots as endpoint_get_all_slots,
)
