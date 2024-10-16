from database.db_handler import DBHandler
from datetime import datetime


class RentalHandler:
    def __init__(self,
                 db_handler: DBHandler):

        self.db_handler = db_handler
        self.cursor = db_handler.cursor

    def create_rental(self, uid, vid, loc_from, status="inuse"):
        self.db_handler.create_query(
            table_name="Rentals",
            fields=("uid", "vid", "starttime", "loc_from", "status"),
            values=[(uid, vid, datetime.now().isoformat(), loc_from, status)]
        )


    def get_rental_by_uid(self, uid, status=None, return_type="dict"):
        if status is None:
            query = f"""
                SELECT * FROM Rentals
                WHERE uid={uid}
            """
        else:
            query = f"""
                SELECT * FROM Rentals
                WHERE uid={uid} and status='{status}'
            """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results is None:
            return None

        if return_type == "dict":
            results = [dict(r) for r in results]
        elif return_type == "object":
            from entities.rental import Rental
            results = [Rental.load_from_dict(dict(r)) for r in results]

        return results

    def get_rental_for_report(self, uid):
        query = f"""
            SELECT * FROM Rentals r, Vehicles v
            WHERE r.uid={uid} AND r.vid =v.id AND r.status='done' 
            AND r.endtime > (SELECT DATETIME('now', '-1 day'))
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results is None:
            return []
        return [dict(r) for r in results]

    def get_rental_info_by_id(self, id: int, return_type="dict"):
        query = f"""
            SELECT * FROM Rentals
            WHERE id = {id}
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if return_type == "dict":
            result = dict(result)
        elif return_type == "object":
            from entities.rental import Rental
            return Rental().load_from_dict(dict(result))
        return result

    # def get_revenue(self,
    #                 status=None,
    #                 year=None,
    #                 group_by="%m-%Y"):
    #     query = f"SELECT SUM(billtotal) as income,
    #     STRFTIME('{group_by}', endtime) as time FROM Rentals"
    #     condition = []
    #     if status is not None:
    #         condition.append(f"status='{status}'")
    #     else:
    #         condition.append("NOT status='inuse'")
    #     if year is not None:
    #         condition.append(f"STRFTIME('%Y', endtime)={year}")
    #     if len(condition) > 0:
    #         query += f" WHERE {'AND'.join(condition)}"
    #
    #     query += f" GROUP BY STRFTIME('{group_by}', endtime)"
    #
    #     self.cursor.execute(query)
    #     results = self.cursor.fetchall()
    #     return [dict(r) for r in results]


    def update_rental(self, rent_id, fields):
        query = f"""
                    UPDATE Rentals
                    SET {", ".join([f"'{k}'='{v}'" if type(v) is str else f"'{k}'={v}"
                                    for k, v in fields.items() if v is not None])}
                    WHERE id = {rent_id}
                """

        self.db_handler.run_query(query)
