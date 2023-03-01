# RT Lib - Config

__all__ = ("IpcsServer", "get_config_file_path")

from typing import TypedDict

from os import getenv

from core.rextlib.common.hash import get_file_hash


class IpcsServer(TypedDict):
    "ipcsのサーバーの接続先の設定の型です。"

    host: str
    port: int


def get_config_file_path() -> str:
    "設定ファイルのパスを取得します。"
    return getenv("RT_CONFIG_FILE_PATH", "config.toml").replace(
        "!config_template_hash!", get_file_hash("core/config/types_.py")
    )