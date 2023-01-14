# RT Lib - Log

from typing import TypeAlias, Literal, TypedDict


__all__ = ("PlaceType", "PlaceValue", "Place")


PlaceType: TypeAlias = Literal["guild", "channel", "url", "other"]
PlaceValue: TypeAlias =  str | None


class Place(TypedDict):
    "ログでログの機能が動作した場所を表すデータの型です。"

    type: PlaceType
    value: PlaceValue