class QueryBuilder:
    """
    SQLを返す関数
    """

    def __init__(self):
        pass

    def create_parent_table(self, table_name):
        return f"""CREATE TABLE {table_name}
        (id UUID DEFAULT gen_random_uuid(),
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

    def create_cid_table_locations_log(self, table_name):
        return f"""CREATE TABLE {table_name}
        (location_id UUID REFERENCES locations(id),
        id UUID,
        location_name TEXT,
        PRIMARY KEY(id));"""

    def insert_parent_datasets(self):
        return f"INSERT INTO locations (id, location_name, address, longitude, latitude) VALUES ($1, $2, $3, $4, $5)"

    def insert_cid_datasets(self):
        return f"INSERT INTO genres (location_id, id, genre) VALUES ($1, $2, $3)"

    def get_location_id(self):
        return "SELECT id FROM locations WHERE location_name = $1;"

    def get_locations_table(self):
        return "SELECT * FROM locations"

    def get_locations(self):
        return "SELECT location_name FROM locations"

    def get_genres(self):
        return """
        SELECT 
            l.id,
            l.location_name,
            g.genre
        FROM locations as l
        LEFT JOIN genres g ON l.id = g.location_id
        WHERE l.id = $1;
        """
