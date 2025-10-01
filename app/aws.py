import psycopg2
import sys
import os
from dotenv import load_dotenv

import pprint
import uuid

import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from DB.database_rds import DatabaseService
from sql.postgresql import QueryBuilder


db_handler.test_connection()
db_handler.show_tables()

# locationテーブルの構造確認
db_handler.show_table_info('location')