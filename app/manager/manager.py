import psycopg2


class FacilityManager:
    def __init__(self):
        conn = psycopg2.connect(
            host="localhost",
            database="prj_tour_route_db",
            user="prj_tour_route_user",
            password="prj_tour_route_password",
            port=9876,
        )
        self.cur = conn.cursor()

    def get_id(self):
        self.cur.execute("SELECT * FROM  places where id = 1")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
