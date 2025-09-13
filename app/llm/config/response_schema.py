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


class PlaceLocation(BaseModel):
    """
    場所の緯度と経度を規定するクラス
    """

    lat: float
    lng: float


class Place(BaseModel):
    """
    個別の場所情報を規定するクラス
    """

    id: str
    name: str
    category: str
    address: str
    distance_meters: int
    location: PlaceLocation
    rating: float
    url: str


class NearbyMetadata(BaseModel):
    """
    メタデータを規定するクラス
    """

    total_results: int
    count: int


class NearbyResponse(BaseModel):
    """
    APIレスポンス全体を規定するクラス
    """

    metadata: NearbyMetadata
    places: list[Place]
