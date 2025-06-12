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


if __name__ == "__main__":
    main()
