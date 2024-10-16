from database.db_handler import DBHandler
from datetime import datetime


class TopupHandler:
    def __init__(self,
                 db_handler: DBHandler):

        self.db_handler = db_handler
        self.cursor = db_handler.cursor

    def create_topup(self, uid, amount):
        self.db_handler.create_query(
            table_name="Topup",
            fields=("uid", "time", "amount"),
            values=[(uid, datetime.now().isoformat(), amount)]
        )

    def get_topup_by_uid(self, uid,):
        query = f"""
            SELECT *
            FROM Topup
            WHERE uid={uid}
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results is None:
            return []

        results = [dict(r) for r in results]
        return results

