class QueryBuilder:
    """
    テーブル作成
    データ挿入

    """
    def __init__(self):
        pass


    def create_table(self):
        return """CREATE TABLE locations
        (location_id INTEGER,
        place_name TEXT,
        address TEXT,
        longitude NUMERIC,
        latitude NUMERIC,
        PRIMARY KEY(location_id));"""

    @property
    def add_record(self):
        return "INSERT INTO places (name, address, latitude, longitude) VALUES (%s, %s, %s, %s)"


