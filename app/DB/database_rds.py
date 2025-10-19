import os
from dotenv import load_dotenv
import asyncpg
from typing import Optional, List, Any
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager

class PostgresCredentials:
    """
    データベース接続情報を保持するクラス
    """
    def __init__(self):
        # .envファイルの正しいパスを指定
        env_path = Path(__file__).parent.parent.parent / ".env"
        load_dotenv(env_path)
        
        # デバッグ: 環境変数の確認
        print(f"🔍 .envファイルパス: {env_path}")
        print(f"🔍 .env存在確認: {env_path.exists()}")
        
        # RDS接続設定（.envから読み込み）
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")  # ← 修正: "v" から "DB_PASSWORD" に
        self.port = int(os.getenv("DB_PORT", "5432"))


class PostgresClient:
    """
    PostgreSQLへ接続するクラス（非同期版）
    """
    def __init__(self):
        self.config = PostgresCredentials()
        self.connection_timeout = 10

    async def connect(self):
        """非同期接続"""
        try:
            print(f"🔄 データベースに接続中: {self.config.host}:{self.config.port}")
            conn = await asyncio.wait_for(
                asyncpg.connect(
                    host=self.config.host,
                    database=self.config.database,
                    user=self.config.user,
                    password=self.config.password,
                    port=self.config.port,
                    ssl='require'  # ← SSL接続を要求
                ),
                timeout=self.connection_timeout
            )
            print("✅ データベース接続成功")
            return conn
        except asyncio.TimeoutError:
            print(f"❌ 接続タイムアウト: {self.connection_timeout}秒以内に接続できませんでした")
            raise Exception(f"接続タイムアウト: {self.connection_timeout}秒以内に接続できませんでした")
        except Exception as e:
            print(f"❌ データベース接続エラー: {e}")
            raise Exception(f"接続エラー: {e}")

    @asynccontextmanage
    async def get_connection_context(self):
        """非同期コネクションのコンテキストマネージャー"""
        conn = None
        try:
            conn = await self.connect()
            yield conn
        except Exception as e:
            print(f"❌ コネクションエラー: {e}")
            raise
        finally:
            if conn:
                await conn.close()
                print("✅ データベース接続終了")


class DatabaseService:
    """
    データベース操作を提供するクラス（非同期版）
    """
    def __init__(self):
        self.client = PostgresClient()

    async def execute_query_fetch(self, query: str, params: Optional[tuple] = None):
        """SELECT文を実行してデータを取得（非同期）"""
        async with self.client.get_connection_context() as conn:
            try:
                print(f"🔄 SELECT実行中: {query[:50]}...")
                
                if params:
                    result = await asyncio.wait_for(
                        conn.fetch(query, *params),
                        timeout=10.0
                    )
                else:
                    result = await asyncio.wait_for(
                        conn.fetch(query),
                        timeout=10.0
                    )
                
                # asyncpgの結果をdict形式に変換
                result_list = [dict(row) for row in result]
                
                print(f"✅ SELECT実行成功: {len(result_list)}行取得")
                return result_list
                
            except asyncio.TimeoutError:
                print("❌ クエリ実行タイムアウト")
                raise Exception("クエリ実行タイムアウト")
            except Exception as e:
                print(f"❌ SELECT実行エラー: {e}")
                raise Exception(f"クエリ実行エラー: {e}")

    async def execute_query(self, query: str, params: Optional[tuple] = None) -> bool:
        """INSERT/UPDATE/DELETE/CREATE文を実行（非同期）"""
        async with self.client.get_connection_context() as conn:
            try:
                print(f"🔄 SQL実行中: {query[:50]}...")
                
                if params:
                    await conn.execute(query, *params)
                else:
                    await conn.execute(query)
                
                # クエリの種類を判定
                query_type = query.strip().split()[0].upper()
                print(f"✅ {query_type}文実行成功")
                
                return True
                
            except Exception as e:
                print(f"❌ SQL実行エラー: {e}")
                print(f"クエリ: {query[:100]}...")
                raise Exception(f"クエリ実行エラー: {e}")

    async def test_connection(self):
        """接続テスト（非同期）"""
        try:
            print("🔄 接続テスト開始...")
            
            async with self.client.get_connection_context() as conn:
                # バージョン確認
                version = await conn.fetchval("SELECT version();")
                
                # データベース情報確認
                db_info = await conn.fetchrow(
                    "SELECT current_database(), current_user, inet_server_addr();"
                )
                
                print("✅ データベース接続テスト成功!")
                print(f"PostgreSQL version: {version[:80]}...")
                print(f"データベース: {db_info['current_database']}")
                print(f"ユーザー: {db_info['current_user']}")
                print(f"サーバーアドレス: {db_info['inet_server_addr']}")
                
                return True
                
        except Exception as e:
            print(f"❌ 接続テストエラー: {e}")
            return False


# テスト実行
if __name__ == "__main__":
    async def main():
        print("=== データベースサービス接続テスト ===\n")
        
        try:
            db_service = DatabaseService()
            
            # 接続テスト
            if await db_service.test_connection():
                print("\n🚀 データベース準備完了！")
            else:
                print("\n❌ データベース接続に失敗しました")
                
        except Exception as e:
            print(f"❌ 初期化エラー: {e}")
            print("\n確認事項:")
            print("1. .envファイルに接続情報が設定されているか")
            print("2. RDSが起動しているか")
            print("3. セキュリティグループが正しく設定されているか")
    
    asyncio.run(main())