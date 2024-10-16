
class User:
    def __init__(self):
        self.role = None
        self.username = None
        self.password = None
        self.dob = None
        self.gender = None
        self.id = None

    def load_from_dict(self, config):
        self.role = config['role']
        self.id = config['id']
        self.username = config['username']
        return self

    def get_username(self):
        return self.username

    def set_password(self, new_password):
        self.password = new_password
        return new_password

    def set_role(self, role):
        if role not in ["customer", "operator", "manager"]:
            return None
        self.role = role
        return role
