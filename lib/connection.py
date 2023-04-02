"RT Common - RT Connection"

__all__ = (
    "get_channel_from_id", "get_shard_ids_from_id", "bot_filter",
    "ConnectionClient"
)

from collections.abc import Iterator

from ipcs import Connection, Client


def get_channel_from_id(id_: str) -> str:
    "IDからチャンネルを取り出します。"
    return id_[:id_.find("_")]


def get_shard_ids_from_id(id_: str) -> Iterator[int]:
    "IDからシャードIDを取り出します。"
    return map(int, id_[id_.find("_")+1:].split(","))


def bot_filter(connection: Connection) -> bool:
    "渡された接続がBotであれば`True`を、そうでなければ`False`を返します。"
    return "_" in connection.id_ and "hq" not in connection.id_


class ConnectionClient(Client):
    "送信先を割り出すための関数を実装したRTコネクション用クライアントのクラスです。"

    def select_all_by_bot(self) -> Iterator[str]:
        "BotのクライアントのIDを返します。"
        for c in self.connections.values():
            if bot_filter(c):
                yield c.id_

    def select_all_by_channel(self, channel: str) -> Iterator[str]:
        "指定されたチャンネルに接続しているクライアントのIDを返します。"
        for id_ in self.connections.keys():
            if id_.startswith(f"{channel}_"):
                yield id_

    def select_by_guild_id(
        self, shard_count: int,
        channel: str, guild_id: int
    ) -> str | None:
        "指定されたチャンネルに接続しているクライアントの中で、指定されたIDのサーバーを管理対象としているクライアントを探します。"
        for id_ in self.select_all_by_channel(channel):
            try:
                for shard_id in get_shard_ids_from_id(id_):
                    if (guild_id >> 22) % shard_count == shard_id:
                        return id_
            except ValueError:
                # 接続するのはBot以外にバックエンドもいる。
                # その場合は`int`変換エラーが発生するからそれをパスする。
                pass

    def get_channels(self) -> Iterator[str]:
        "接続しているクライアントのチャンネルを全て返します。"
        yielded = set[str]()
        for id_ in self.connections:
            if "_" not in id_:
                continue
            if (channel := get_channel_from_id(id_)) not in yielded:
                yielded.add(channel)
                yield channel