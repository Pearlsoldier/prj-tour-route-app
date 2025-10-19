import os
from dotenv import load_dotenv
import asyncpg
import asyncio
from contextlib import asynccontextmanager
from typing import Optional, List, Any


class PostgresCredentials:
    """
    データベース接続情報
        （ホスト名、DB名、ユーザー名、パスワード、ポート）
    を保持するクラス
    """

    def __init__(self):
        load_dotenv("../../.env")

        self.host = os.getenv("host")
        self.database = os.getenv("database")
        self.user = os.getenv("user")
        self.password = os.getenv("password")
        self.port = os.getenv("port")
        self.ssl_mode = "disable"  # ローカル環境
        # self.ssl_mode = 'require'  # 本番環境


class PostgresClient:
    """
    PostgresCredentialsを使って、
    実際にPostgreSQLへ接続するクラス
    コネクションの生成や管理を担当
    """

    def __init__(self):
        self.config = PostgresCredentials()
        self.connection_timeout = 10.0
        self.query_timeout = 30.0

    async def connect(self):
        try:
            conn = await asyncio.wait_for(
                asyncpg.connect(
                    host=self.config.host,
                    database=self.config.database,
                    user=self.config.user,
                    password=self.config.password,
                    port=self.config.port,
                    ssl=se,
                ),
                timeout=self.connection_timeout,
            )
            return conn
        except asyncio.TimeoutError:
            raise Exception(
                f"接続タイムアウト: {self.connection_timeout}秒以内に接続できませんでした"
            )
        except Exception as e:
            raise Exception(f"接続エラー: {e}")

    @asynccontextmanager
    async def get_connection_context(self):
        conn = None
        try:
            conn = await self.connect()
            yield conn
        finally:
            if conn:
                await conn.close()


class DatabaseService:
    """
    非同期処理で行う
    PostgresClientを使って、
    アプリケーションが必要とするDB操作
    （例：データ取得、保存など）を提供するクラス
    """

    def __init__(self):
        self.client = PostgresClient()

    async def execute_query_fetch(self, query: str, params: Optional[tuple] = None):
        async with self.client.get_connection_context() as conn:
            try:
                result = await asyncio.wait_for(
                    conn.fetch(query, *(params or ())),
                    timeout=self.client.query_timeout,
                )
                return result
            except asyncio.TimeoutError:
                raise Exception(
                    f"クエリタイムアウト: {self.client.query_timeout}秒以内に完了しませんでした"
                )
            except Exception as e:
                raise Exception(f"クエリ実行エラー: {e}")

    async def execute_query(self, query: str, params: Optional[tuple] = None) -> bool:
        """INSERT/UPDATE/DELETE文を実行"""
        async with self.client.get_connection_context() as conn:
            try:
                await asyncio.wait_for(
                    conn.execute(query, *(params or ())),
                    timeout=self.client.query_timeout,
                )
                return True
            except asyncio.TimeoutError:
                raise Exception(
                    f"クエリタイムアウト: {self.client.query_timeout}秒以内に完了しませんでした"
                )
            except Exception as e:
                raise Exception(f"クエリ実行エラー: {e}")
