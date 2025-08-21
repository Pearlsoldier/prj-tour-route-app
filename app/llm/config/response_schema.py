from pydantic import BaseModel


class GeminiResponse(BaseModel):
    """
    Geminiのレスポンスを規定するクラス
    """

    response: str
    is_continue_conversation: bool


class RouteResponse(BaseModel):
    """
    Routeのレスポンスを規定するクラス
    """
    response: str
    coordinates: list
