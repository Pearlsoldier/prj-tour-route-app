# lib/endpoints.py - 純粋な定数
class GSIEndpoints:
    GEOCODING_BASE_URL = "https://msearch.gsi.go.jp/address-search"
    REVERSE_GEOCODING_BASE_URL = "https://mreversegeocoder.gsi.go.jp/reverse-geocoder"
    DISTANCE_CALC_BASE_URL = "https://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc"

# config/settings.py - 実際の設定
class APISettings:
    # 環境によって変わりうる設定
    TIMEOUT = 30
    RETRY_COUNT = 3
    DEBUG = False
    
    # デフォルト値（設定として扱う）
    DEFAULT_ELLIPSOID = "GRS80"
    DEFAULT_OUTPUT_TYPE = "json"