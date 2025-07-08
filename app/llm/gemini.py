import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List

from prompts import system_prompt, user_prompt

user_input = input()

# .envファイルの読み込み
load_dotenv()

# API-KEYの設定
API_KEY = os.getenv("API_KEY")


class GeminiResponse(BaseModel):
    response: str
    is_continue_conversation: bool


# クライアントの初期化
client = genai.Client(api_key=API_KEY)

# コンテンツ生成の実行
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=user_prompt,
    config=genai.types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json",
        response_schema=GeminiResponse.model_json_schema(),
    ),
)

# 結果の表示
