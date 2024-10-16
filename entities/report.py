class Report:
    def __init__(self):
        self.id = None
        self.uid = None
        self.vid = None
        self.time = None
        self.fix_time = None
        self.detail = None
        self.status = None

    def load_from_dict(self, config):
        self.id = config.get('id', None)
        self.uid = config.get('uid', None)
        self.vid = config.get('vid', None)
        self.time = config.get('time', None)
        self.fix_time = config.get('fix_time', None)
        self.detail = config.get('detail', None)
        self.status = config.get('status', None)

        return self

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'vid': self.vid,
            'time': self.time,
            'fix_time': self.fix_time,
            'detail': self.detail,
            'status': self.status
        }

    def __str__(self):
        from utils.datetime_utils import beautify_time
        import utils.db_utils as db

        vehicle = db.vehicle_handler.get_vehicle_info_by_id(id=self.vid)
        user = db.user_handler.get_user_info_by_id(id=self.uid)
        return f"""
            REPORT DETAILS
            
        Vehicle: {vehicle['type']}-{self.vid}
        Reported by: {user['username']}
        Report Time: {beautify_time(self.time)}
        Details: {self.detail}
        Status: {self.status}
        """