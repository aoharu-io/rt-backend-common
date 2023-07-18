"rtlib - Event Log"

__all__ = ("ResultType", "RESULT_TYPES", "PlaceType", "PlaceValue", "Place", "Feature")

from typing import TypeAlias, Literal, get_args

from typing_extensions import TypedDict


ResultType: TypeAlias = Literal["error", "warning", "success", "unknown"]
RESULT_TYPES: tuple[ResultType, ...]  = get_args(ResultType)

PlaceType: TypeAlias = Literal["guild", "channel", "url", "other"]
PlaceValue: TypeAlias =  str | None

class Place(TypedDict):
    "イベントログでログの機能が動作した場所を表すデータの型です。"

    type: PlaceType
    "ログの発生源の種類です。"
    value: PlaceValue
    "場所を割り出すための情報です。例えば`.type`が`guild`の場合、ここにはIDを入れます。"

class Feature(TypedDict):
    "機能情報のデータの型です。"

    name: str
    "名前へのlocaleのキーです。"
    dashboard: str | None
    "ダッシュボードへのパスです。"
    document: str | None
    "ドキュメントへのパスです。"