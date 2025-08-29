from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

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
async def start_chat(request: ChatStartRequest):
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
                genres2=loc.get("genres2", "")
            )
            locations.append(accessible_location)

        # ChatInterfaceを使用して対話開始
        builder = ClientBuilder
        gemini_model = builder.set_up_model()
        gemini_contents = builder.create_contents(user_input=request.user_input)
        gemini_system_prompt = builder.create_system_instruction(
            system_prompt=dialogue_system_prompt,
            location_datasets=locations
        )
        gemini_config = builder.create_config(
            gemini_system_instruction=gemini_system_prompt
        )

        gemini_chat = ChatInterface(
            model=gemini_model, 
            config=gemini_config, 
            contents=gemini_contents
        )
        chat_response = gemini_chat.start_chat()
        
        # テスト用の簡単なレスポンス
        return ChatResponse(
            response=chat_response.text if hasattr(chat_response, 'text') else str(chat_response),
            continue_conversation=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat start failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Tour Route API is running"}

@app.get("/chat/{user_input}")
async def chat_get(user_input: str):
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
            system_prompt=dialogue_system_prompt,
            location_datasets=locations
        )
        gemini_config = builder.create_config(
            gemini_system_instruction=gemini_system_prompt
        )

        gemini_chat = ChatInterface(
            model=gemini_model, 
            config=gemini_config, 
            contents=gemini_contents
        )
        chat_response = gemini_chat.start_chat()
        
        return {
            "user_input": user_input,
            "response": chat_response.text if hasattr(chat_response, 'text') else str(chat_response),
            "continue_conversation": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
    
@app.get("/places/nearby")
async def search_places(request: Request):
    full_url = str(request.url)
    print(f"Full URL: {full_url}")
    return {"original_url": full_url}


    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8999)