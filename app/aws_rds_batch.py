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
from batch.preprocessing import RegistrationInformation
from location.locations import Location, Coordinate

        
if __name__ == "__main__":
    sql_handler = QueryBuilder()
    db_handler = DatabaseService()
    # print("何件登録しますか？")
    # input_num = int(input())
    # print(f"{input_num}件の施設情報を登録します")
    # for i in range(input_num):
    #     id = uuid.uuid4()
    #     location_name = input()
    #     id_location_name = (id, location_name)
    #     redistration_location = RegistrationInformation(location_name)
    #     address, lon, lat = redistration_location.get_geocoding()
    #     params = (str(id), location_name, address, lon, lat)
    get_locatios_table = sql_handler.get_locations()
    print(db_handler.execute_query_fetch(get_locatios_table))
    print("施設名を入力してください")
    input_location = input()
    location_obj = Location(input_location)
    location_obj_id_query = sql_handler.get_location_id(location_obj.location)
    location_obj_id = db_handler.execute_query_fetch(location_obj_id_query, (location_obj.location,))
    id = location_obj_id[0][0]
    cid_id = str(uuid.uuid4())
    print(id)
    print(cid_id)
    print("ジャンルを入力してください")
    genre = input()
    cid_registration = sql_handler.insert_cid_datasets()
    insert_genres = db_handler.execute_query(cid_registration, (id, cid_id, genre))
    get_genres = sql_handler.get_table("genres")
    print(db_handler.execute_query_fetch(get_genres))

