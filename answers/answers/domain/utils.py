from functools import partial

from shortuuid import ShortUUID

_short_uuid = ShortUUID()
length = None

new_id = partial(_short_uuid.random, length=length)
