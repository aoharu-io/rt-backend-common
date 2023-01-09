# RT Lib - Extended Cacher

from __future__ import annotations

from typing import Any, cast

from ipcs import Client

from ...rextlib.common.cacher import Cacher, KeyT, ValueT
from ...rextlib.common.utils import Executors


def _setup_reset_all_cache(self: BackendControllableCacher) -> None:
    global _setup_is_done
    if _setup_is_done:
        return
    _setup_is_done = True

    # 全てのキャッシュを消す指示をバックエンドから受け取れるようにする。

    def _reset_cacheof_bc_cachers() -> None:
        for bc_cacher in _bc_cachers:
            bc_cacher.clear()

    @self.connection.route()
    async def reset_cache_of_bc_cacher(_) -> None:
        await self.connection.loop.run_in_executor(
            self.executors.normal, _reset_cacheof_bc_cachers
        )


class BackendControllableCacher(Cacher[KeyT, ValueT]):
    """ipcsのRouteを設定してバックエンドが簡単にキャッシュを消せるようにしたCacherです。"""

    connection: Client = cast(Any, None)
    executors: Executors = cast(Any, None)

    def __init__(self, name: str, *args: Any, **kwargs: Any) -> None:
        if self.connection is None:
            raise RuntimeError("IPCSのクライアントのインスタンスが`.connection`に格納されていません。")
        if self.executors is None:
            raise RuntimeError("`.executors`が設定されていません。")
        if not isinstance(name, str):
            raise TypeError("第一引数`name`は文字列である必要があります。")

        super().__init__(*args, **kwargs)

        self.connection.set_route(self._remove_cache, f"remove_{name}_cache_of_bc_cacher")
        _bc_cachers.append(self)
        _setup_reset_all_cache(self)

    def _remove_cache(self, _, key: Any, assassinate: bool = False) -> bool:
        try:
            if assassinate:
                self.default_on_dead(key, None)
            else:
                del self[key]
        except KeyError:
            return False
        return True
_setup_is_done, _bc_cachers = False, list[BackendControllableCacher]()