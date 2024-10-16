class Topup:
    def __init__(self):
        self.id = None
        self.uid = None
        self.time = None
        self.amount = None

    def load_from_dict(self, config):
        self.id = config.get('id', None)
        self.uid = config.get('uid', None)
        self.time = config.get('time', None)
        self.amount = config.get('amount', None)

        return self

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'time': self.time,
            'fix_time': self.amount,
        }

    def __str__(self):
        return """
            
        """

