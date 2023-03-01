# RT Lib - Config

from typing import TypedDict


__all__ = ("IpcsServer",)


class IpcsServer(TypedDict):
    "ipcsのサーバーの接続先の設定の型です。"

    host: str
    port: int