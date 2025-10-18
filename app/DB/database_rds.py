import os
from dotenv import load_dotenv
import psycopg2
from typing import Optional, List, Any
from contextlib import contextmanager
from pathlib import Path


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
        
        # SSHトンネル経由の接続設定
        self.host = "localhost"  # SSHトンネル経由
        self.database = "postgres"
        self.user = "postgres" 
        self.password = os.getenv("AWS_RDS_PASSWORD")
        self.port = 15432  # SSHトンネルのローカルポート
        
        # パスワードの確認


class PostgresClient:
    """
    PostgreSQLへ接続するクラス
    """
    def __init__(self):
        self.config = PostgresCredentials()
        self.connection_timeout = 10

    def connect(self):
        try:
            print(f"🔄 データベースに接続中: {self.config.host}:{self.config.port}")
            conn = psycopg2.connect(
                host=self.config.host,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
                port=self.config.port,
                connect_timeout=self.connection_timeout
            )
            print("✅ データベース接続成功")
            return conn
        except psycopg2.OperationalError as e:
            print(f"❌ データベース接続エラー: {e}")
            raise Exception(f"接続エラー: {e}")
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")
            raise Exception(f"接続エラー: {e}")

    @contextmanager
    def get_connection_context(self):
        """コネクションのコンテキストマネージャー"""
        conn = None
        try:
            conn = self.connect()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
                print("🔄 トランザクションをロールバック")
            raise
        finally:
            if conn:
                conn.close()
                print("✅ データベース接続終了")


class DatabaseService:
    """
    データベース操作を提供するクラス
    """
    def __init__(self):
        self.client = PostgresClient()

    def execute_query_fetch(self, query: str, params: Optional[tuple] = None):
        """SELECT文を実行してデータを取得"""
        with self.client.get_connection_context() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                columns = [desc[0] for desc in cursor.description]
                print(f"🔍 columns: {columns}")
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]
                cursor.close()
                
                print(f"✅ SELECT実行成功: {len(result)}行取得")
                return result
                
            except Exception as e:
                print(f"❌ SELECT実行エラー: {e}")
                raise Exception(f"クエリ実行エラー: {e}")

    def execute_query(self, query: str, params: Optional[tuple] = None) -> bool:
        """INSERT/UPDATE/DELETE/CREATE文を実行"""
        with self.client.get_connection_context() as conn:
            try:
                cursor = conn.cursor()
                
                print(f"🔄 SQL実行中: {query[:50]}...")
                cursor.execute(query, params or ())
                conn.commit()
                cursor.close()
                
                # クエリの種類を判定
                query_type = query.strip().split()[0].upper()
                print(f"✅ {query_type}文実行成功")
                
                return True
                
            except psycopg2.Error as e:
                conn.rollback()
                print(f"❌ PostgreSQLエラー: {e}")
                print(f"クエリ: {query[:100]}...")
                raise Exception(f"PostgreSQLエラー: {e}")
            except Exception as e:
                conn.rollback()
                print(f"❌ SQL実行エラー: {e}")
                print(f"クエリ: {query[:100]}...")
                raise Exception(f"クエリ実行エラー: {e}")

    def execute_sql_file(self, file_path: str) -> bool:
        """SQLファイルを実行"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"❌ SQLファイルが見つかりません: {file_path}")
            return False
        
        try:
            print(f"🔄 SQLファイル実行開始: {file_path.name}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            # セミコロンでクエリを分割
            queries = [query.strip() for query in sql_content.split(';') if query.strip()]
            
            success_count = 0
            for i, query in enumerate(queries, 1):
                try:
                    print(f"\n  📝 クエリ {i}/{len(queries)} 実行中...")
                    self.execute_query(query)
                    success_count += 1
                except Exception as e:
                    print(f"  ❌ クエリ {i} 実行失敗: {e}")
                    print(f"  失敗したクエリ: {query[:100]}...")
                    return False
            
            print(f"\n✅ SQLファイル実行完了: {file_path.name} ({success_count}個のクエリ実行)")
            return True
            
        except Exception as e:
            print(f"❌ ファイル実行エラー: {e}")
            return False

    def show_tables(self):
        """テーブル一覧を表示"""
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """
        try:
            results = self.execute_query_fetch(query)
            print("\n📋 現在のテーブル一覧:")
            if results:
                for table in results:
                    print(f"  - {table[0]}")
            else:
                print("  テーブルが見つかりません")
            return [table[0] for table in results]
        except Exception as e:
            print(f"❌ テーブル一覧取得エラー: {e}")
            return []

    def show_table_info(self, table_name: str):
        """テーブル構造を表示"""
        query = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position;
        """
        try:
            results = self.execute_query_fetch(query, (table_name,))
            
            if results:
                print(f"\n📋 テーブル '{table_name}' の構造:")
                print("  カラム名 | データ型 | NULL許可 | デフォルト値")
                print("  " + "-" * 60)
                for col in results:
                    print(f"  {col[0]} | {col[1]} | {col[2]} | {col[3] or 'なし'}")
            else:
                print(f"❌ テーブル '{table_name}' が見つかりません")
                
        except Exception as e:
            print(f"❌ テーブル情報取得エラー: {e}")

    def test_connection(self):
        """接続テスト"""
        try:
            print("🔄 接続テスト開始...")
            
            with self.client.get_connection_context() as conn:
                cursor = conn.cursor()
                
                # バージョン確認
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                
                # データベース情報確認
                cursor.execute("SELECT current_database(), current_user, inet_server_addr();")
                db_info = cursor.fetchone()
                
                cursor.close()
                
                print("✅ データベース接続テスト成功!")
                print(f"PostgreSQL version: {version[0][:80]}...")
                print(f"データベース: {db_info[0]}")
                print(f"ユーザー: {db_info[1]}")
                print(f"サーバーアドレス: {db_info[2]}")
                
                return True
                
        except Exception as e:
            print(f"❌ 接続テストエラー: {e}")
            return False


# テスト実行
if __name__ == "__main__":
    print("=== データベースサービス接続テスト ===\n")
    
    try:
        db_service = DatabaseService()
        
        # 接続テスト
        if db_service.test_connection():
            print("\n🚀 データベース準備完了！")
            
            # テーブル一覧表示
            db_service.show_tables()
            
            print("\n📖 使用方法:")
            print("  db_service.execute_query('CREATE TABLE ...')")
            print("  db_service.execute_sql_file('path/to/script.sql')")
            print("  db_service.show_tables()")
            
        else:
            print("\n❌ データベース接続に失敗しました")
            
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        print("\n確認事項:")
        print("1. SSHトンネルが実行中か")
        print("2. .envファイルにAWS_RDS_PASSWORDが設定されているか")
        print("3. RDSが起動しているか")