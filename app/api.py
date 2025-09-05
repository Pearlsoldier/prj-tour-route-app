from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from dotenv import load_dotenv

import asyncpg
import asyncio

from DB.database import PostgresClient, DatabaseService

from urllib.parse import urlparse

from fastapi import FastAPI, Request, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, parse_qs, unquote
from pydantic import BaseModel, Field
import json

# パス設定
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.interface import ClientBuilder, ChatInterface
from location.locations import AccessibleLocation
from llm.prompts.dialogue_prompts import dialogue_system_prompt
from llm.prompts.nearby_location import nearby_system_prompt

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
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.message
            }
        }
    )


@app.post("/chat/start", response_model=ChatResponse)
def start_chat(request: ChatStartRequest):
    """
    対話セッションを開始する
    """
    try:
        # location_dataをAccessibleLocationオブジェクトに変換
        locations = []
        for loc in request.location_data:
            accessible_location = AccessibleLocation(
                location_name=loc.get("location_name", ""),
                genres1=loc.get("genres1", ""),
                genres2=loc.get("genres2", ""),
            )
            locations.append(accessible_location)

        # ChatInterfaceを使用して対話開始
        builder = ClientBuilder
        gemini_model = builder.set_up_model()
        gemini_contents = builder.create_contents(user_input=request.user_input)
        gemini_system_prompt = builder.create_system_instruction(
            system_prompt=dialogue_system_prompt, location_datasets=locations
        )
        gemini_config = builder.create_config(
            gemini_system_instruction=gemini_system_prompt
        )

        gemini_chat = ChatInterface(
            model=gemini_model, config=gemini_config, contents=gemini_contents
        )
        chat_response = gemini_chat.start_chat()

        # テスト用の簡単なレスポンス
        return ChatResponse(
            response=(
                chat_response.text
                if hasattr(chat_response, "text")
                else str(chat_response)
            ),
            continue_conversation=True,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat start failed: {str(e)}")


@app.get("/")
def root():
    return {"message": "Tour Route API is running"}


@app.get("/chat/{user_input}")
def chat_get(user_input: str):
    """
    GETリクエストでチャットができるエンドポイント
    例: http://localhost:8999/chat/こんにちは
    """
    try:
        # 空のlocation_dataでチャット開始
        locations = []

        # ChatInterfaceを使用して対話開始
        builder = ClientBuilder
        gemini_model = builder.set_up_model()
        gemini_contents = builder.create_contents(user_input=user_input)
        gemini_system_prompt = builder.create_system_instruction(
            system_prompt=dialogue_system_prompt, location_datasets=locations
        )
        gemini_config = builder.create_config(
            gemini_system_instruction=gemini_system_prompt
        )

        gemini_chat = ChatInterface(
            model=gemini_model, config=gemini_config, contents=gemini_contents
        )
        chat_response = gemini_chat.start_chat()

        return {
            "user_input": user_input,
            "response": (
                chat_response.text
                if hasattr(chat_response, "text")
                else str(chat_response)
            ),
            "continue_conversation": True,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.get("/places/nearby")
async def search_places(
    q: str = Query(...,  description="検索の基準となる地名やランドマーク名", examples="東京駅"),
    radius: Optional[int] = Query(1000, description="検索半径（メートル）", examples=500),
    category: Optional[str] = Query(None, description="場所のカテゴリを指定（例: カフェ、レストラン、公園など）", examples="cafe"),
    limit: Optional[int] = Query(10, description="取得する最大の件数。指定しない場合はデフォルト値（例: 20）を適用", examples=10)
    ):
    """
    GETリクエストのエンドポイント
    例: http://localhost:8999/places/nearby?q=東京駅&radius=500&category=cafe
    """
    if not q:
        raise CustomHttpException(400, "必須パラメータ 'q' が指定されていません。")
    load_dotenv()
    try:
        start_position = Location(q)
        start_location_name = start_position.location
        start_lat = float(start_position.latitude)
        start_lon = float(start_position.longitude)
        start_address = start_position.address

        accessible_locations = []
        
        def is_accessible(locations_distance: float, radius: int):
            return locations_distance < radius
        
        sql_handler = QueryBuilder()
        db_handler = DatabaseService()

        client = PostgresClient()

        locations_query = sql_handler.get_locations_table()
        locations_table = await db_handler.execute_query_fetch(locations_query)


        async with client.get_connection_context() as conn:
            result = await conn.fetch("SELECT version()")
        
        print(f"locations_table: {locations_table}")

        within_range_locations = []

        

        print(f"locations_table :{locations_table}")
        for location_record in locations_table:
            end_location_name = location_record['location_name']
            location_id = location_record['id']
            end_lat = float(location_record['latitude'])
            end_lon = float(location_record['longitude'])
            location_address = location_record['address']

            if start_location_name == end_location_name:
                # print(f"end : {end_location}")
                continue
            get_genres_query = sql_handler.get_genres()
            genres_table = await db_handler.execute_query_fetch(
                get_genres_query, (location_id,) 
            )
            locations_distance = LocationsDistance(
                start_location=start_location_name,
                end_location=end_location_name
            )
            distance = locations_distance.locations_distance
            if is_accessible(locations_distance=distance, radius=radius):
                end_location_handler = Location(end_location_name)
                location_and_genres = AccessibleLocation(
                    end_location_handler.location,
                    end_location_handler.address
                )
                accessible_locations.append(end_location_name)
        return {
            "metadata":{
                "total_results": len(locations_table),
                "count": len(accessible_locations)
            },
            "places": {
                "name": location_and_genres.locations_name,
                "adress": location_and_genres.adress
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8999)
