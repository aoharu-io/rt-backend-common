"RT Lib - Log"

__all__ = ("set_output_handler",)

from os import getenv
from pathlib import PurePath

from logging import Logger

from core.rextlib.common.log import set_output_handler as original_set_output_handler


def set_output_handler(
    logger: Logger, id_: str = "",
    default: str = "data/logs/main!id!.log"
) -> None:
    """ログの出力を設定します。
    出力先のファイルパスは`RT_LOG_PATH`で変更が可能です。
    そのパスにもし`!id!`を入れた場合、この関数の引数`id`の値で交換がされます。"""
    original_set_output_handler(logger, PurePath(
        getenv("RT_LOG_PATH", default).replace("!id!", id_)
    ))