class QueryBuilder:
    """
    テーブル作成
    データ挿入

    """
    def __init__(self):
        pass

    @property
    def create_table(self):
        return """SELECT table_name
        , constraint_name
        , constraint_type
        FROM information_schema.table_constraints
        WHERE table_name = %s
        AND (constraint_type = 'PRIMARY KEY' OR constraint_type = 'FOREIGN KEY');"""
    
    @property
    def add_record(self):
        return "INSERT INTO places (name, address, latitude, longitude) VALUES (%s, %s, %s, %s)"


