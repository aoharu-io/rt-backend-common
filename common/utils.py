# RT Lib - Utils

from time import time
from uuid import uuid4


__all__ = ("SignatureTool",)


class SignatureTool:
    "署名を作るためのクラスです。"

    def __init__(self, cmcls) -> None:
        with open("secret.key", "rb") as f:
            self.chiper = cmcls(f.read())

    def make_auth_headers(self) -> dict:
        "Bot専用APIを使う際に必要なヘッダーを作ります。"
        return {"Authorization": "Rt %s" % self.signature}

    @property
    def signature(self) -> str:
        "Bot専用のバックエンドのエンドポイントへのアクセスに使用する署名を返します。"
        return self.chiper.encrypt(f"RT-Discord-Bot_{time()}_{uuid4()}")