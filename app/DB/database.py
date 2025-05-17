import os
from dotenv import load_dotenv
import psycopg


class PostgresCredentials:
    """
    データベース接続情報
        （ホスト名、DB名、ユーザー名、パスワード、ポート）
    を保持するクラス
    """

    def __init__(self):
        load_dotenv("../../.env")

        self.host = os.getenv("host")
        self.dbname = os.getenv("database")
        self.user = os.getenv("user")
        self.password = os.getenv("password")
        self.port = os.getenv("port")


class PostgresClient:
    """
    PostgresCredentialsを使って、
    実際にPostgreSQLへ接続するクラス
    コネクションの生成や管理を担当
    """

    def __init__(self):
        self.config = PostgresCredentials()

    def connect(self):
        try:
            self.conn = psycopg.connect(
                host=self.config.host,
                dbname=self.config.dbname,
                user=self.config.user,
                password=self.config.password,
                port=self.config.port,
            )
            self.cur = self.conn.cursor()
            return True
        except Exception as e:
            print(f"接続に失敗しました{e}")
            return False

    def execute(self, query, params=None):
        """SQLクエリを実行するメソッド"""
        self.cur.execute(query, params)
        return self.cur

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()


class DatabaseService:
    """
    PostgresClientを使って、
    アプリケーションが必要とするDB操作
    （例：データ取得、保存など）を提供するクラス
    """

    def __init__(self):
        self.client = PostgresClient()

    def execute_query_fetch(self, query, params=None):
        try:
            if self.client.connect():
                cursor = self.client.execute(query, params)
                result = cursor.fetchall()
                self.client.commit()
                self.client.close()
                return result
            return False
        except Exception as e:
            print(f"失敗しました。{e}")
            return False

    def execute_query(self, query, params=None):
        try:
            if self.client.connect():
                self.client.execute(query, params)
                self.client.commit()
                self.client.close()
                return True
            return False
        except Exception as e:
            print(f"失敗しました。{e}")
            return False
