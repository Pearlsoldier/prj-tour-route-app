import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from typing import List

from prompts import system_prompt, user_prompt

# .envファイルの読み込み
load_dotenv()

# API-KEYの設定
API_KEY = os.getenv("API_KEY")


class GeminiResponse(BaseModel):
    """
    Geminiのレスポンスを規定するクラス
    """

    response: str
    is_continue_conversation: bool


class ConversationMessage(BaseModel):
    """
    会話の１メッセージを規定する
    roleは、ユーザーかGeminiか
    """

    role: str
    content: str


class SessionManager(BaseModel):
    """
    Geminiとユーザーの会話を管理するクラス
    """

    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.location_datas
        self.chat_logs: List[ConversationMessage] = []
        self.session_active = False

    def initialize_session(self, location_datas):
        self.location_datas = location_datas
        self.session_active = True
        self.chat_logs = []
        return "施設情報の設定を完了しました。"

    def add_user_message(self, user_input):
        message = ConversationMessage(role="user", content=user_input)
        self.chat_logs.append(message)

    def add_gemini_message(self, response):
        message = ConversationMessage(role="gemini", content=response)
        self.chat_logs.append(message)

    def generate_response(
        self, user_input, user_prompt, system_prompt
    ) -> GeminiResponse:

        self.add_user_message(user_input)
        self.user_prompt = user_prompt
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(system_instruction=system_prompt),
            contents=user_prompt,
        )
