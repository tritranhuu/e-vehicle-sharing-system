import sqlite3


class DBHandler:
    def __init__(self, db_name):
        with sqlite3.connect(db_name) as db:
            self.db = db
            self.db.row_factory = sqlite3.Row
            self.cursor = db.cursor()
        self.init_db()
    def init_db(self):
        # create table Users
        query = """
            CREATE TABLE IF NOT EXISTS Users(
                id integer PRIMARY KEY AUTOINCREMENT,
                username text NOT NULL UNIQUE,
                password text NOT NULL,
                dob text,
                phone text,
                balance real NOT NULL,
                role text NOT NULL,
                status text NOT NULL
            );
            """
        self.cursor.execute(query)

        # create table Vehicles
        query = """
            CREATE TABLE IF NOT EXISTS Vehicles(
                id integer PRIMARY KEY AUTOINCREMENT,
                type text NOT NULL,
                location text NOT NULL,
                battery integer NOT NULL,
                status text NOT NULL
            );
        """
        self.cursor.execute(query)

        #create table Rentals
        query = """
            CREATE TABLE IF NOT EXISTS Rentals(
                id integer PRIMARY KEY AUTOINCREMENT,
                uid integer,
                vid integer,
                starttime text,
                endtime text,
                loc_from text,
                loc_to text,
                billtotal real,
                status text,
                FOREIGN KEY(uid) REFERENCES Users(id),
                FOREIGN KEY(vid) REFERENCES Vehicles(id)
            );
        """
        self.cursor.execute(query)

        #create table Reports
        query = """
            CREATE TABLE IF NOT EXISTS Reports(
                id integer PRIMARY KEY AUTOINCREMENT,
                rid integer,
                time text,
                detail text,
                repair_time text,
                status text,
                FOREIGN KEY(rid) REFERENCES Rentals(id)   
            )
        """
        self.cursor.execute(query)

        # create table Top-up
        query = """
                CREATE TABLE IF NOT EXISTS Topup(
                    id integer PRIMARY KEY AUTOINCREMENT,
                    uid integer,
                    time text,
                    amount text,
                    FOREIGN KEY(uid) REFERENCES Users(id)
                )
            """
        self.cursor.execute(query)

    def create_query(self, table_name, values, fields=None):
        query = f"""
            INSERT INTO {table_name}
            {str(fields) if fields is not None else ""}
            VALUES {",".join([str(value) for value in values])}
        """
        # print(query)
        self.cursor.execute(query)
        self.db.commit()

    def dalete_query(self, table, fields: dict, logic_exp="AND"):
        query = f"""
            DELETE FROM {table}
            WHERE {logic_exp.join([f"'{k}'='{v}'" if type(v) is str else f"'{k}'={v}"
                                   for k, v in fields.items()])}
        """
        self.cursor.execute(query)
        self.db.commit()

    def run_query(self, query):
        self.cursor.execute(query)
        self.db.commit()


if __name__ == '__main__':
    db = DBHandler("EVehicle.db")
