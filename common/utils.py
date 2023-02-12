"rtlib - Utils"

__all__ = (
    "SignatureTool", "CodeRunner", "dumps_object_to_str", "loads_object_from_str",
    "Plan"
)

from typing import TypeVar, Generic, Protocol, Any
from collections.abc import Callable, Coroutine

from concurrent.futures import ThreadPoolExecutor
from asyncio import AbstractEventLoop

from base64 import b64encode, b64decode
import pickle

from time import time
from uuid import uuid4


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


def dumps_object_to_str(obj: object, *args: Any, **kwargs: Any) -> str:
    "pickleでオブジェクトをbytesにして、それをbase64で文字列にします。"
    return b64encode(pickle.dumps(obj, *args, **kwargs)).decode()
def loads_object_from_str(raw: str, *args: Any, **kwargs: Any) -> object:
    "`.dumps_object_to_str`の逆です。"
    return pickle.loads(b64decode(raw.encode()))


class CustomerManagerProtocol(Protocol):
    "`.Plan`を使う上で顧客管理用クラスに実装していないといけないことをまとめたプロトコルのクラスです。"

    async def check(self, guild_id: int) -> bool:
        "指定されたサーバーIDのサーバーがプラスを購読している稼働かを返します。"
        ...

ValueT = TypeVar("ValueT")
class Plan(Generic[ValueT]):
    "プランの設定を格納するための適切な設定を返すための関数を実装したクラスです。"

    _customers: CustomerManagerProtocol

    def __init__(self, free: ValueT, plus: ValueT) -> None:
        self.free, self.plus = free, plus

    async def judge(self, guild_id: int) -> ValueT:
        "指定されたサーバーIDに適切な値を返します。"
        return self.plus if await self._customers.check(guild_id) else self.free