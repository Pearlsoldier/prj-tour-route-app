import os
from dotenv import load_dotenv
import google.generativeai as genai

# .envファイルの読み込み
load_dotenv()

# API-KEYの設定
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

gemini_pro = genai.GenerativeModel("gemini-2.0-flash")
prompt = "こんにちは"
response = gemini_pro.generate_content(prompt)
print(response.text)
