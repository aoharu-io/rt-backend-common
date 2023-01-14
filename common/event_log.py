# RT Lib - Event Log

from typing import TypeAlias, Literal, TypedDict, get_args


__all__ = ("ResultType", "RESULT_TYPES", "PlaceType", "PlaceValue", "Place")


ResultType: TypeAlias = Literal["error", "warning", "success", "unknown"]
PlaceType: TypeAlias = Literal["guild", "channel", "url", "other"]
PlaceValue: TypeAlias =  str | None
RESULT_TYPES: tuple[ResultType, ...]  = get_args(ResultType)


class Place(TypedDict):
    "イベントログでログの機能が動作した場所を表すデータの型です。"

    type: PlaceType
    value: PlaceValue