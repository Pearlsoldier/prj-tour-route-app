import sys
import os
import pprint
import uuid

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from DB.database import DatabaseService
from sql.postgresql import QueryBuilder
from preprocessing import DatabasePreprocessing


def main():

    sql_handler = QueryBuilder()

    uuid.uuid4
    # batch_insert = sql_handler.insert_cid_datasets()
    locations_tabale_query = sql_handler.get_locations_table()
    db_handler = DatabaseService()
    locations_table = db_handler.execute_query_fetch(locations_tabale_query)
    print(f"locations_table: {locations_table}")
    print(locations_table[0][0])
    for i in range(len(locations_table)):
        print(locations_table[i][0])
        print(locations_table[i][1])
        location_id = str(locations_table[i][0])
        genres = sql_handler.get_genres(locations_table[i][0])
        locations_genres = db_handler.execute_query_fetch(genres, (location_id,))
        print(locations_genres)

    # for i in range(len(locations_table)):
    #     print(locations_table[i][0])
    #     print(locations_table[i][1])
    #     location_id = locations_table[i][0]
    #     genres = sql_handler.get_genres(location_id)

    #     # デバッグ: 実際のSQLクエリを出力
    #     print("Generated SQL:")
    #     print(repr(genres))  # repr()で改行文字なども表示
    #     print("Parameter:", location_id)
    #     print("Parameter type:", type(location_id))

    #     locations_genres = db_handler.execute_query_fetch(genres, (location_id, ))
    #     print(locations_genres)
    #     break  # 最初の1件だけテスト


if __name__ == "__main__":
    main()
