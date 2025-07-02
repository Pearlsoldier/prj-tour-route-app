import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# .envファイルの読み込み
load_dotenv()

# API-KEYの設定
API_KEY = os.getenv("API_KEY")


# クライアントの初期化
client = genai.Client(api_key=API_KEY)

# コンテンツ生成の実行
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="富士山とは何ですか？",
    config=types.GenerateContentConfig(
        system_instruction="ツアーコンダクターとして解説してください。"
    ),
)

# 結果の表示
print(response.text)
