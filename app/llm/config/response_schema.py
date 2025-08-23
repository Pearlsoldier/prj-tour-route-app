from pydantic import BaseModel


class ChatResponse(BaseModel):
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
