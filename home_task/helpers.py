import typing

import orjson


def orjson_dumps(v: typing.Any, *, default: typing.Any) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode(encoding="utf-8")
