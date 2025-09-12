from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from dotenv import load_dotenv

from llm.config.config import Config


from DB.database import PostgresClient, DatabaseService

from urllib.parse import urlparse

from fastapi import FastAPI, Request, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, parse_qs, unquote
from pydantic import BaseModel, Field
import json

from llm.interface import ChatInterface, ClientBuilder
from llm.prompts.route_prompts import route_system_prompt, route_user_prompt
# パス設定
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.interface import ClientBuilder, ChatInterface
from location.locations import AccessibleLocation

from metrics_module.metrics import LocationsDistance
from DB.database import DatabaseService
from sql.postgresql import QueryBuilder
from location.locations import Location, AccessibleLocation


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
async def search_route(
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

        locations_query = sql_handler.get_locations_table()

        locations_table = await db_handler.execute_query_fetch(locations_query)

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

        for location_record in locations_table:
            end_location_name = location_record["location_name"]
            location_id = location_record["id"]
            end_lat = float(location_record["latitude"])
            end_lon = float(location_record["longitude"])
            location_address = location_record["address"]

            if start_location_name == end_location_name:
                # print(f"end : {end_location}")
                continue
            locations_distance = LocationsDistance(
                start_location=start_location_name, end_location=end_location_name
            )
            distance = locations_distance.locations_distance
            if is_accessible(locations_distance=distance, radius=radius):
                end_location_handler = Location(end_location_name)
                accessible_locations.append({
                    "name": end_location_handler.location,
                    "address": end_location_handler.address,
                    "location": {
                        "lat": end_location_handler.longitude,
                        "lng": end_location_handler.latitude
                        }
                    })
        print(accessible_locations)
        if len(accessible_locations) == 0:
            return {
                "metadata": {
                    "total_results": len(locations_table),
                    "count": 0,
                },
                "places": [],
                "message": "指定された範囲内に場所が見つかりませんでした",
            }
        user_input = accessible_locations
        builder = ClientBuilder
        gemini_model = builder.set_up_model()
        gemini_contents = builder.create_contents(user_input=user_input)
        print("🟢")
        gemini_system_instruction = builder.create_system_instruction(route_system_prompt)
        gemini_config = builder.create_config(gemini_system_instruction)
        print("🟥")

        gemini_chat = ChatInterface(
            model=gemini_model, config=gemini_config, contents=gemini_contents
        )
        print("🟦")
        chat = gemini_chat.start_chat()
        return {"Gemini": chat.parsed.response}
    except CustomHttpException:
        print("CustomHttpExceptionを再発生")
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


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
    例: http://localhost:8999/route/search?q=東京駅&radius=5000&category=cafe
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

        locations_query = sql_handler.get_locations_table()

        locations_table = await db_handler.execute_query_fetch(locations_query)

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

        for location_record in locations_table:
            end_location_name = location_record["location_name"]
            location_id = location_record["id"]
            end_lat = float(location_record["latitude"])
            end_lon = float(location_record["longitude"])
            location_address = location_record["address"]

            if start_location_name == end_location_name:
                # print(f"end : {end_location}")
                continue
            locations_distance = LocationsDistance(
                start_location=start_location_name, end_location=end_location_name
            )
            distance = locations_distance.locations_distance
            if is_accessible(locations_distance=distance, radius=radius):
                end_location_handler = Location(end_location_name)
                AccessibleLocation(
                    end_location_handler.location, end_location_handler.address
                )
                accessible_locations.append(end_location_name)
        print(accessible_locations)
        if len(accessible_locations) == 0:
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
                "count": len(accessible_locations),
            },
            "places": accessible_locations,
        }
    except CustomHttpException:
        print("CustomHttpExceptionを再発生")
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8999)
