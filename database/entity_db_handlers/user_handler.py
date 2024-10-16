from database.db_handler import DBHandler


class UserHandler:
    def __init__(self,
                 db_handler: DBHandler):

        self.db_handler = db_handler
        self.cursor = db_handler.cursor

    def create_user(self, username, password, dob="", phone="", role="customer"):
        self.db_handler.create_query(table_name="Users",
                                     fields=("username", "password", "dob", "phone", "balance", "role", "status"),
                                     values=[(username, password, dob, phone, 0, role, "active")])

    def get_all_user(self, return_type="dict"):
        query = """SELECT * FROM Users WHERE status='active'"""

        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results is None:
            return None
        if return_type == "dict":
            results = [dict(r) for r in results]
        elif return_type == "object":
            from entities.user import User
            results = [User.load_from_dict(dict(r)) for r in results]

        return results

    def update_user_by_id(self,
                    user_id: int,
                    fields: dict):
        query = f"""
            UPDATE Users
            SET {", ".join([f"'{k}'='{v}'" if type(v) is str else f"'{k}'={v}"
                            for k, v in fields.items()])}
            WHERE id = {user_id}
        """
        self.db_handler.run_query(query)

    def delete_user_by_id(self, user_id: int):
        query = f"DELETE FROM Users WHERE id={user_id}"
        self.db_handler.run_query(query)

    def get_user_by_username(self,
                             username: str,
                             return_type="dict"
                             ):
        query = f"""
            SELECT * FROM Users
            WHERE username = '{username}'
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is None:
            return None

        if return_type == "object":
            from entities.user import User
            user = User.load_from_dict(dict(result))
            return user
        elif return_type == "dict":
            result = dict(result)

        return result

    def get_user_info_by_id(self, id: int, return_type="dict"):
        query = f"""
            SELECT * FROM Users
            WHERE id = {id}
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        if return_type == "dict":
            result = dict(result)
        return result
    # def delete_user_by_id(self, user_id: int):

    # def get_rental_history(self):





if __name__ == '__main__':
    db_handler = DBHandler("../database/EVehicle.db")
    user_controller = UserHandler(db_handler)
    # user_controller.create_user("trith", "123", role="admin")
    user_controller.update_user_by_id(2, {"role": "customer"})