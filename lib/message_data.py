# RT Lib - Message Data

from __future__ import annotations

from typing import TypedDict, TypeAlias, Any


__all__ = ("AbsoluteAuthor", "RelativeAuthor", "AuthorType", "MessageData")


class AbsoluteAuthor(TypedDict):
    "送信者の設定の型です。"

    name: str
    "ユーザー名です。"
    avatar_url: str
    "アバターのURLです。"


RelativeAuthor: TypeAlias = int
AuthorType: TypeAlias = AbsoluteAuthor | RelativeAuthor
class MessageData(TypedDict):
    "メッセージの内容を表すデータの型です。"

    author: AuthorType
    "送信者の設定です。"
    body: dict[str, Any]
    "メッセージの本体です。"