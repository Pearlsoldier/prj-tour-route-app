import psycopg3


class FacilityManager:
    def __init__(self):
        pass

    def get_id(self):
        self.cur.execute("SELECT * FROM  places where id = 1")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
