from database.db_handler import DBHandler
from datetime import datetime


class ReportHandler:
    def __init__(self,
                 db_handler: DBHandler):

        self.db_handler = db_handler
        self.cursor = db_handler.cursor

    def create_report(self, rid, detail="", status="pending"):
        self.db_handler.create_query(
            table_name="Reports",
            fields=("rid", "time", "detail", "status"),
            values=[(rid, datetime.now().isoformat(), detail, status)]
        )

    def get_report_by_uid(self, uid, status=None):
        if status is None:
            query = f"""
                SELECT *
                FROM Reports r, Rentals rent
                WHERE r.rid = rent.id AND rent.uid = {uid}
            """
        else:
            query = f"""
                SELECT *
                FROM Reports r, Rentals rent
                WHERE r.rid = rent.id AND rent.uid = {uid} AND r.status={status}
            """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results is None:
            return []

        results = [dict(r) for r in results]
        return results

    def get_current_by_vid(self, vid, return_type="dict"):

        query = f"""
            SELECT *
            FROM Reports r, Rentals rent
            WHERE r.rid = rent.id AND rent.vid = {vid} AND r.status='pending'
        """
        self.cursor.execute(query)

        results = self.cursor.fetchone()
        if results is None:
            return None
        if return_type == "dict":
            results = dict(results)
        elif return_type == "object":
            from entities.report import Report
            return Report().load_from_dict(dict(results))
        return results


    def update_report(self, rep_id, fields):
        query = f"""
                    UPDATE Reports
                    SET {", ".join([f"'{k}'='{v}'" if type(v) is str else f"'{k}'={v}"
                                    for k, v in fields.items()])}
                    WHERE id = {rep_id}
                """
        self.db_handler.run_query(query)


