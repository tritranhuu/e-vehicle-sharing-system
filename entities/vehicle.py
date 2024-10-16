class Vehicle:
    def __init__(self):
        self.type = None
        self.id = None
        self.location = None
        self.battery = None
        self.status = None

    def load_from_dict(self, config):
        self.type = config['type']
        self.id = config['id']
        self.location = config['location']
        self.battery = config['battery']
        self.status = config['status']

        return self

    def __str__(self):
        return f"{self.id} - {self.type} - Battery: {self.battery}%"
