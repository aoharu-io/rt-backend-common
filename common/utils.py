# RT Lib - Utils

from typing import Any
from collections.abc import Callable, Coroutine

from concurrent.futures import ThreadPoolExecutor
from asyncio import AbstractEventLoop

from time import time
from uuid import uuid4


__all__ = ("SignatureTool", "CodeRunner")


class SignatureTool:
    "署名を作るためのクラスです。"

    def __init__(self, cmcls) -> None:
        with open("secret.key", "rb") as f:
            self.secret_key = f.read()
        self.chiper = cmcls(self.secret_key)

    def make_auth_headers(self) -> dict:
        "Bot専用APIを使う際に必要なヘッダーを作ります。"
        return {"Authorization": "Rt %s" % self.signature}

    @property
    def signature(self) -> str:
        "Bot専用のバックエンドのエンドポイントへのアクセスに使用する署名を返します。"
        return self.chiper.encrypt(f"RT-Discord-Bot_{time()}_{uuid4()}")


class CodeRunner:
    "文字列状態のコードを動かすための関数を実装したクラスです。"

    def __init__(
        self, loop: AbstractEventLoop,
        executor: ThreadPoolExecutor | None = None
    ) -> None:
        self.loop, self.executor = loop, executor or ThreadPoolExecutor(2)

    def update_globals(self, _: dict[str, Any]) -> None:
        "コード内で使える変数を編集するための辞書が渡される関数です。"

    def _generate_function(self, code: str, globals_: dict[str, Any]) -> Callable[[], Coroutine]:
        # 指定されたコードを実行するコルーチン関数を作ります。
        exec("async def _run_go():\n  {}".format(code.replace("\n", "\n  ")), globals_)
        return globals_["_run_go"]

    async def run(self, code: str, **globals_: Any) -> Any:
        "指定されたコードを非同期で実行します。"
        self.update_globals(globals_)
        return await (await self.loop.run_in_executor(
            self.executor, self._generate_function, code, globals_
        ))()

    async def _rn(self, _, code: str) -> str:
        # ipcs用。
        return repr(await self.run(code))