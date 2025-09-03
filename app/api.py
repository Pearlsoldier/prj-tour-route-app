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
                locations_name=loc.get("locations_name", ""),
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
async def search_places(request: Request):
    """
    GETリクエストでチャットができるエンドポイント
    例: http://localhost:8999/places/nearby?q=東京駅&radius=500&category=cafe
    """
    database_service = PostgresClient()
    try:
        client = PostgresClient()

        async with client.get_connection_context() as conn:
            result = await conn.fetch("SELECT version()")

        return {
            "status": "connection successful",
            "database_version": result[0] if result else "No result",
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}

    # full_url = str(request.url)
    # parsed = urlparse(full_url)
    # params = parse_qs(parsed.query)
    # if 'q' not in params or not params['q'][0]:
    #     raise ValueError("必須パラメータ'q'が指定されていません")

    # result = {
    #         'start_position': params['q'][0],
    #         'radius': int(params['radius'][0]) if 'radius' in params else 1000,
    #         'category': params['category'][0] if 'category' in params else None,
    #         'limit': int(params['limit'][0]) if 'limit' in params else 20
    #     }
    # start_position = result['start_position']

    # load_dotenv()

    # def is_accessible(locations_distance: float, radius: int):
    #     return locations_distance < radius

    # # 移動手段と所有時間から移動可能圏内を導く
    # sql_handler = QueryBuilder()
    # locations_tabale_query = sql_handler.get_locations_table()
    # db_handler = DatabaseService()
    # locations_table = db_handler.execute_query_fetch(locations_tabale_query)
    # # print(f"locations_table: {locations_table}")
    # within_range_locations = []
    # start_position = Location(start_position)
    # start_location = start_position.location

    # accessible_locations = []

    # for i in range(len(locations_table)):
    #     locations_name = locations_table[i][1]
    #     locations_id = locations_table[i][0]
    #     end_location = locations_name

    #     if start_location == end_location:
    #         # print(f"end : {end_location}")
    #         continue
    #     get_genres_query = sql_handler.get_genres(end_location)
    #     genres_table = db_handler.execute_query_fetch(
    #         get_genres_query, params=(locations_table[i][0],)
    #     )
    #     locations_distance = LocationsDistance(
    #         start_location=start_location,
    #         end_location=end_location
    #     )
    #     distance = locations_distance.locations_distance
    #     if is_accessible(locations_distance=distance, radius=result['radius']):
    #         end_location_handler = Location(end_location)
    #         locations_name = genres_table[0][1]
    #         location_and_genres = AccessibleLocation(
    #             end_location_handler.location,
    #             end_location_handler.address
    #         )
    #         accessible_locations.append(locations_name)
    # return {
    #     "metadata":{
    #         "total_results": len(locations_table),
    #         "count": len(accessible_locations)
    #     },
    #     "places": {
    #         "name": location_and_genres.locations_name,
    #         "adress": location_and_genres.adress
    #     }
    # }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8999)
