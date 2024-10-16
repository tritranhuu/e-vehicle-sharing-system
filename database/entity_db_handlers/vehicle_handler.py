from database.db_handler import DBHandler


class VehicleHandler:
    def __init__(self,
                db_handler: DBHandler):

        self.db_handler = db_handler
        self.cursor = db_handler.cursor

    def create_vehicle(self, type, location, battery=100, status="available"):
        self.db_handler.create_query(
            table_name="Vehicles",
            fields=("type", "location", "battery", "status"),
            values=[(type, location, battery, status)]
        )

    def update_vehicle_by_id(self,
                    vehicle_id: int,
                    fields: dict):
        query = f"""
            UPDATE Vehicles
            SET {", ".join([f'"{k}"="{v}"' if type(v) is str else f"'{k}'={v}"
                            for k, v in fields.items()])}
            WHERE id = {vehicle_id}
        """
        self.db_handler.run_query(query)

    def get_all_vehicles(self, return_type="dict"):
        query = f"""
                SELECT * FROM Vehicles
                WHERE NOT status='deleted'
            """
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if return_type == "dict":
            results = [dict(r) for r in results]
        elif return_type == "object":
            from entities.vehicle import Vehicle
            return [Vehicle().load_from_dict(dict(r)) for r in results]
        return results

    def get_all_avail_vehicles(self, return_type="dict"):
        query = f"""
            SELECT * FROM Vehicles
            WHERE NOT status='unavailable'
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if return_type == "dict":
            results = [dict(r) for r in results]
        elif return_type == "object":
            from entities.vehicle import Vehicle
            return [Vehicle().load_from_dict(dict(r)) for r in results]
        return results

    def get_vehicle_info_by_id(self, id: int, return_type="dict"):
        query = f"""
            SELECT * FROM Vehicles
            WHERE id = {id}
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if return_type == "dict":
            result = dict(result)
        return result

    def get_vehicles_by_location(self,
                                 location: str,
                                 return_type="dict",
                                 status="available"):
        if status is None:
            query = f"""
                SELECT * FROM Vehicles
                WHERE location = '{location}' AND NOT status='deleted'
            """
        else:
            query = f"""
                SELECT * FROM Vehicles
                WHERE location = '{location}' AND status='{status}'
            """
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if return_type == "dict":
            results = [dict(r) for r in results]
        elif return_type == "object":
            from entities.vehicle import Vehicle
            return [Vehicle().load_from_dict(dict(r)) for r in results]
        return results

    def get_locations_of_vehicle(self):
        query = """
            SELECT location, count(id) as num_vehicle FROM Vehicles
            WHERE NOT status='deleted' 
            GROUP BY location
            ORDER BY count(id) DESC
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return [dict(r) for r in results]

    def get_vehicles_by_battery(self, battery=10):
        query = f"""
            SELECT * FROM Vehicles
            WHERE battery < {battery} AND NOT status='deleted'
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results is None:
            return []
        return [dict(r) for r in results]

    def get_defective_vehicles(self):
        query = f"""
            SELECT * FROM Vehicles
            WHERE status='defective'
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results is None:
            return []
        return [dict(r) for r in results]
