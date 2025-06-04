class QueryBuilder:
    """
    SQLを返す関数
    """

    def __init__(self):
        pass

    def create_parent_table(self, table_name):
        return f"""CREATE TABLE {table_name}
        (id UUID DEFEAULT,
        location_name TEXT,
        address TEXT,
        longitude NUMERIC,
        latitude NUMERIC,
        PRIMARY KEY(id));"""

    def create_cid_table(self, table_name):
        return f"""CREATE TABLE {table_name}
        (location_id UUID REFERENCES locations(id),
        id UUID,
        genre TEXT,
        PRIMARY KEY(id));"""

    def insert_parent_datasets(self, table_name):
        return f"INSERT INTO {table_name} (id, location_name, address, longitude, latitude) VALUES (%s, %s, %s, %s, %s)"

    def insert_cid_datasets(self, table_name):
        return f"INSERT INTO {table_name} (location_id, id, genre) VALUES (%s, %s, %s)"

    def get_location_id(self):
        return "SELECT id FROM locations WHERE location_name = %s;"

    def get_locations_table(self):
        return "SELECT * FROM locations"
    
    def get_locations(self):
        return "SELECT location_name FROM locations"
    
    def get_genres(self, location_id):
        return """
        SELECT 
            l.id,
            l.location_name,
            STRING_AGG(g.genre, ',') as genre
        FROM locations as l
        LEFT JOIN genres g ON l.id = g.location_id
        where l.id = %s
        GROUP BY l.id, l.location_name;
        """