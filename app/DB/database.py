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
        print(
            f"PostgresClient: host={self.config.host}, db={self.config.dbname}, user={self.config.user}, port={self.config.port}"
        )

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

    def execute(self, query, values=None):
        """SQLクエリを実行するメソッド"""
        self.cur.execute(query, (values))
        return self.cur

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()

    # def execute(self, sql):
    # try:
    #     if self.client.connect():
    #         self.client.execute(sql)
    #         self.client.commit()
    #         self.client.close()
    #         return True
    #     return False
    # except Exception as e:
    #     print(f"失敗しました。{e}")
    # return False


class DatabaseService:
    """
    PostgresClientを使って、
    アプリケーションが必要とするDB操作
    （例：データ取得、保存など）を提供するクラス
    """

    def __init__(self):
        self.client = PostgresClient()
        self.conn = self.client.connect()

    def get_id(self):
        self.client.cur.execute("SELECT * FROM  places where id = 1")
        rows = self.client.cur.fetchall()
        for row in rows:
            print(row)

    def add_column(self):
        try:
            if self.client.connect():
                self.client.execute("ALTER TABLE facility_genres ADD COLUMN name TEXT")
                self.client.commit()
                self.client.close()
                return True
            return False
        except Exception as e:
            print(f"失敗しました。{e}")
            return False

    def add_value(self, place_mane, address, latitude, longitude):
        sql = "INSERT INTO places (name, address, latitude, longitude) VALUES (%s, %s, %s, %s)"
        try:
            if self.client.connect():
                self.client.execute(sql, (place_mane, address, latitude, longitude))
                self.client.commit()
                self.client.close()
                return True
            return False
        except Exception as e:
            print(f"追加に失敗しました。{e}")
            return False

    def rename_column(self):
        sql = "ALTER TABLE places RENAME COLUMN adress TO address"
        try:
            if self.client.connect():
                self.client.execute(sql)
                self.client.commit()
                self.client.close()
                return True
            return False
        except Exception as e:
            print(f"失敗しました。{e}")
            return False

    def re_type(self):
        sql = "ALTER TABLE places ALTER COLUMN longitude TYPE NUMERIC USING longitude::NUMERIC"
        try:
            if self.client.connect():
                self.client.execute(sql)
                self.client.commit()
                self.client.close()
                return True
            return False
        except Exception as e:
            print(f"失敗しました。{e}")
            return False

    def drop_column(self):
        sql = "ALTER TABLE places DROP COLUMN hogehoge"
        try:
            if self.client.connect():
                self.client.execute(sql)
                self.client.commit()
                self.client.close()
                return True
            return False
        except Exception as e:
            print(f"失敗しました。{e}")
            return False
    
    def add_table(self):
        sql = """CREATE TABLE facility_genres (
        id SERIAL PRIMARY KEY,
        main_genre VARCHAR(10),
        sub_genre_1 VARCHAR(10),
        sub_genre_2 VARCHAR(10)
        )"""
        try:
            if self.client.connect():
                self.client.execute(sql)
                self.client.commit()
                self.client.close()
                return True
            return False
        except Exception as e:
            print(f"失敗しました。{e}")
        return False

    def check_constraints(self):
        sql = """SELECT table_name
        , constraint_name
        , constraint_type
        FROM information_schema.table_constraints
        WHERE table_name = 'places'
        AND (constraint_type = 'PRIMARY KEY' OR constraint_type = 'FOREIGN KEY') ;"""
        try:
            if self.client.connect():
                cursor = self.client.execute(sql)
                results = cursor.fetchall()
                self.client.commit()
                self.client.close()
                return results
            return False
        except Exception as e:
            print(f"失敗しました。{e}")
        return False
    
    def configuring_foreign_key(self):
        sql = """ALTER TABLE places
        ADD CONSTRAINT fk_place_category
        FOREIGN KEY (name) REFERENCES facility_genres(name);"""
        try:
            if self.client.connect():
                cursor = self.client.execute(sql)
                results = cursor.fetchall()
                self.client.commit()
                self.client.close()
                return results
            return False
        except Exception as e:
            print(f"失敗しました。{e}")
            return False


    def make_sql(self):
        pass

