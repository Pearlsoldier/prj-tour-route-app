import os
import asyncio
import asyncpg
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from typing import Optional, List, Any

class PostgresCredentials:
    """データベース接続情報を保持するクラス"""
    
    def __init__(self):
        load_dotenv("../../.env")
        
        self.host = os.getenv("host", "localhost")
        self.database = os.getenv("database")  # asyncpgでは'database'
        self.user = os.getenv("user")
        self.password = os.getenv("password")
        self.port = int(os.getenv("port", 5432))
        self.ssl_mode = "disable"  # ローカル環境

class AsyncPostgresClient:
    """非同期PostgreSQL接続クライアント"""
    
    def __init__(self):
        self.config = PostgresCredentials()
        self.connection_timeout = 10.0
        self.query_timeout = 30.0
    
    async def get_connection(self):
        """タイムアウト付きでDB接続を取得"""
        try:
            conn = await asyncio.wait_for(
                asyncpg.connect(
                    host=self.config.host,
                    port=self.config.port,
                    user=self.config.user,
                    password=self.config.password,
                    database=self.config.database,
                    ssl=self.config.ssl_mode
                ),
                timeout=self.connection_timeout
            )
            return conn
        except asyncio.TimeoutError:
            raise Exception(f"接続タイムアウト: {self.connection_timeout}秒以内に接続できませんでした")
        except Exception as e:
            raise Exception(f"接続エラー: {e}")
    
    @asynccontextmanager
    async def get_connection_context(self):
        """コンテキストマネージャーとしてDB接続を提供"""
        conn = None
        try:
            conn = await self.get_connection()
            yield conn
        finally:
            if conn:
                await conn.close()

class AsyncDatabaseService:
    """非同期データベース操作サービス"""
    
    def __init__(self):
        self.client = AsyncPostgresClient()
    
    async def execute_query_fetch(self, query: str, params: Optional[tuple] = None) -> List[Any]:
        """SELECT文を実行して結果を取得"""
        async with self.client.get_connection_context() as conn:
            try:
                result = await asyncio.wait_for(
                    conn.fetch(query, *(params or ())),
                    timeout=self.client.query_timeout
                )
                return result
            except asyncio.TimeoutError:
                raise Exception(f"クエリタイムアウト: {self.client.query_timeout}秒以内に完了しませんでした")
            except Exception as e:
                raise Exception(f"クエリ実行エラー: {e}")
    
    async def execute_query(self, query: str, params: Optional[tuple] = None) -> bool:
        """INSERT/UPDATE/DELETE文を実行"""
        async with self.client.get_connection_context() as conn:
            try:
                await asyncio.wait_for(
                    conn.execute(query, *(params or ())),
                    timeout=self.client.query_timeout
                )
                return True
            except asyncio.TimeoutError:
                raise Exception(f"クエリタイムアウト: {self.client.query_timeout}秒以内に完了しませんでした")
            except Exception as e:
                raise Exception(f"クエリ実行エラー: {e}")