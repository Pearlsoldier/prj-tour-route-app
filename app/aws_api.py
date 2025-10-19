from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from dotenv import load_dotenv

from llm.config.config import Config


from DB.database_rds import DatabaseService

from urllib.parse import urlparse

from fastapi import FastAPI, Request, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, parse_qs, unquote
from pydantic import BaseModel, Field
import json

from location.locations import TouristSpot

from llm.interface import ChatInterface, ClientBuilder
from llm.prompts.route_prompts import route_system_prompt, route_user_prompt

# パス設定
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.interface import ClientBuilder, ChatInterface
from location.locations import AccessibleLocation

from metrics_module.metrics import LocationsDistance
from sql.postgresql import QueryBuilder
from location.locations import Location, AccessibleLocation, TouristSpot, Places


app = FastAPI(title="Tour Route API", version="1.0.0")


class ChatStartRequest(BaseModel):
    user_input: str
    location_data: Optional[List[dict]] = []


class ChatResponse(BaseModel):
    response: str
    continue_conversation: bool


class SearchParams(BaseModel):
    q: str


class CustomHttpException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.exception_handler(CustomHttpException)
async def custom_http_exception_handler(request: Request, exc: CustomHttpException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.status_code, "message": exc.message}},
    )


@app.get("/route/search")
# async def search_route(
#     q: str = Query(
#         ..., description="検索の基準となる地名やランドマーク名", examples="東京駅"
#     ),
#     radius: Optional[int] = Query(
#         1000, description="検索半径（メートル）", examples=500
#     ),
#     category: Optional[str] = Query(
#         None,
#         description="場所のカテゴリを指定（例: カフェ、レストラン、公園など）",
#         examples="cafe",
#     ),
#     limit: Optional[int] = Query(
#         10,
#         description="取得する最大の件数。指定しない場合はデフォルト値（例: 20）を適用",
#         examples=10,
#     ),
# ):
#     if not q:
#         raise CustomHttpException(400, "必須パラメータ 'q' が指定されていません。")
#     load_dotenv()
#     try:
#         start_position = Location(q)
#         start_location_name = start_position.location
#         print(start_location_name)

#         accessible_locations = []

#         def is_accessible(locations_distance: float, radius: int):
#             return locations_distance < radius

#         sql_handler = QueryBuilder()
#         db_handler = DatabaseService()

#         locations_query = sql_handler.get_table("locations")
        
#         locations_table = await db_handler.execute_query_fetch(locations_query)

#         ## ここでクエリの施設名がデータベースにないときにエラーをライズ
#         is_station = False
#         print(f"検索対象: '{start_location_name}'")
#         print(f"データベース内の場所一覧:")

#         for location_record in locations_table:
#             print(f"  - '{location_record['location_name']}'")
#             if start_location_name == location_record["location_name"]:
#                 print(f"✅ 一致: {location_record['location_name']}")
#                 is_station = True
#                 break

#         print(f"is_station結果: {is_station}")

#         if is_station == False:
#             print("404エラーを発生させます")
#             raise CustomHttpException(
#                 404, f"指定された地名 '{start_location_name}' が見つかりませんでした。"
#             )

#         for location_record in locations_table:
#             end_location_name = location_record["location_name"]

#             if start_location_name == end_location_name:
#                 # print(f"end : {end_location}")
#                 continue
#             locations_distance = LocationsDistance(
#                 start_location=start_location_name, end_location=end_location_name
#             )
#             distance = locations_distance.locations_distance
#             if is_accessible(locations_distance=distance, radius=radius):
#                 end_location_handler = Location(end_location_name)
#                 accessible_locations.append(
#                     {
#                         "name": end_location_handler.location,
#                         "address": end_location_handler.address,
#                         "location": {
#                             "lat": end_location_handler.longitude,
#                             "lng": end_location_handler.latitude,
#                         },
#                     }
#                 )
#         print(accessible_locations)
#         if len(accessible_locations) == 0:
#             return {
#                 "metadata": {
#                     "total_results": len(locations_table),
#                     "count": 0,
#                 },
#                 "places": [],
#                 "message": "指定された範囲内に場所が見つかりませんでした",
#             }
#         user_input = accessible_locations
#         builder = ClientBuilder
#         gemini_model = builder.set_up_model()
#         gemini_contents = builder.create_contents(
#             user_input=user_input, start_position=start_location_name
#         )
#         gemini_system_instruction = builder.create_system_instruction(
#             route_system_prompt
#         )
#         gemini_config = builder.create_config(gemini_system_instruction)

#         gemini_chat = ChatInterface(
#             model=gemini_model, config=gemini_config, contents=gemini_contents
#         )
#         chat = gemini_chat.start_chat()
#         try:
#             return {"Gemini": chat["response"]}
#         except Exception as e:
#             print(f"テキスト取得エラー: {e}")
#             return {"Gemini": str(chat)}
#     except CustomHttpException:
#         print("CustomHttpExceptionを再発生")
#         raise
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/places/nearby")
async def search_places(
    q: str = Query(
        ..., description="検索の基準となる地名やランドマーク名", examples="東京駅"
    ),
    radius: Optional[int] = Query(
        1000, description="検索半径（メートル）", examples=500
    ),
    category: Optional[str] = Query(
        None,
        description="場所のカテゴリを指定（例: カフェ、レストラン、公園など）",
        examples="cafe",
    ),
    limit: Optional[int] = Query(
        10,
        description="取得する最大の件数。指定しない場合はデフォルト値（例: 20）を適用",
        examples=10,
    ),
):
    """
    GETリクエストのエンドポイント
    例: http://13.231.51.232:8999/places/nearby?q=東京駅&radius=5000&category=レジャー
    例: http://localhost/places/nearby?q=東京駅&radius=5000&category=文化施設
    """
    if not q:
        raise CustomHttpException(400, "必須パラメータ 'q' が指定されていません。")
    load_dotenv()
    try:
        start_position = Location(q)
        start_location_name = start_position.location
        print(start_location_name)

        accessible_locations = []

        def is_accessible(locations_distance: float, radius: int):
            return locations_distance < radius

        sql_handler = QueryBuilder()
        db_handler = DatabaseService()

        # locations_query = sql_handler.get_locations()
        locations_query = sql_handler.get_table("locations")



        locations_table = await db_handler.execute_query_fetch(locations_query)


        # locations_table = await db_handler.execute_query_fetch(locations_query)
        print(locations_table[0])
        print(type(locations_table[0]))

        ## ここでクエリの施設名がデータベースにないときにエラーをライズ
        is_station = False
        print(f"検索対象: '{start_location_name}'")
        print(f"データベース内の場所一覧:")

        for location_record in locations_table:
            print(f"  - '{location_record['location_name']}'")
            if start_location_name == location_record["location_name"]:
                print(f"✅ 一致: {location_record['location_name']}")
                is_station = True
                break

        print(f"is_station結果: {is_station}")

        if is_station == False:
            print("404エラーを発生させます")
            raise CustomHttpException(
                404, f"指定された地名 '{start_location_name}' が見つかりませんでした。"
            )

        tourist_spots = []
        for location_record in locations_table:
            genres = []
            end_location_name = location_record["location_name"]
            location_id = location_record["id"]
            end_lat = float(location_record["latitude"])
            end_lon = float(location_record["longitude"])
            location_address = location_record["address"]
            get_genres_query = sql_handler.get_genres()
            genres_table = await db_handler.execute_query_fetch(
                get_genres_query, (location_id,)
            )
            for genre_record in genres_table:
                genres.append(genre_record["genre"])
            tourist_spot = TouristSpot(
                locations_id=location_id,
                locations_name=end_location_name,
                address=location_address,
                longitude=end_lon,
                latitude=end_lat,
                genres=genres
            )
            
            if start_location_name == tourist_spot.locations_name:
                # print(f"end : {end_location}")
                continue
            locations_distance = LocationsDistance(
                start_location=start_location_name,
                end_location=tourist_spot.locations_name
            )
            print(f"category: {category}")
            print(f"genres: {genres}")
            distance = locations_distance.locations_distance
            if is_accessible(locations_distance=distance,
                             radius=radius):
                for genre in genres:
                    if category == genre:
                        print(f"category: {category}")
                        print(f"genres: {genres}")
                        tourist_spots.append(tourist_spot)
        if len(tourist_spots) == 0:
            return {
                "metadata": {
                    "total_results": len(locations_table),
                    "count": 0,
                },
                "places": [],
                "message": "指定された範囲内に場所が見つかりませんでした",
            }
        return {
            "metadata": {
                "total_results": len(locations_table),
                "count": len(tourist_spots),
            },
            "places": tourist_spots,
        }
    except CustomHttpException:
        print("CustomHttpExceptionを再発生")
        raise
    except ValueError as e:
        print(f"ValueError発生: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"予期しないエラー発生: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8999)