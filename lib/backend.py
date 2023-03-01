"RT Lib - バックエンドのためのライブラリです。"

__all__ = ("is_bot", "IPCS_SERVER_ID")

from core.rextlib.common.chiper import ChiperManager


IPCS_SERVER_ID = "BEACON"
def is_bot(chiper: ChiperManager, credentials: str) -> bool:
    "Botかどうかをチェックします。"
    try:
        word, _, _ = chiper.decrypt(credentials[3:]).split("_")
    except Exception:
        word = ""
    if word == "RT-Discord-Bot":
        return True
    return False