__all__ = ("set_file_handler",)

from os import getenv
from pathlib import PurePath

from logging import Logger

from core.rextlib.common.log import set_file_handler as original_set_file_handler


def set_file_handler(
    logger: Logger, id_: str = "",
    default: str = "data/logs/!id!.log"
) -> None:
    """ログの出力を設定します。
    出力先のファイルパスは`RT_LOG_PATH`で変更が可能です。
    そのパスにもし`!id!`を入れた場合、この関数の引数`id`の値で交換がされます。"""
    original_set_file_handler(logger, PurePath(
        getenv("RT_LOG_PATH", default).replace("!id!", id_)
    ))