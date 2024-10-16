class Rental:
    def __init__(self):
        self.id = None
        self.uid = None
        self.vid = None
        self.start_time = None
        self.end_time = None
        self.loc_from = None
        self.loc_to = None
        self.bill_total = None
        self.status = None

    def load_from_dict(self, config):
        self.id = config.get('id', None)
        self.uid = config.get('uid', None)
        self.vid = config.get('vid', None)
        self.start_time = config.get('starttime', None)
        self.end_time = config.get('endtime', None)
        self.end_time = config.get('endtime', None)
        self.loc_from = config.get('loc_from', None)
        self.loc_to = config.get('loc_to', None)
        self.bill_total = config.get('billtotal', None)
        self.status = config.get('status', None)

        return self

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'vid': self.vid,
            'starttime': self.start_time,
            'endtime': self.end_time,
            'loc_from': self.loc_from,
            'loc_to': self.loc_to,
            'billtotal': self.bill_total,
            'status': self.status
        }

    def get_detail(self):
        from datetime import datetime
        from utils.datetime_utils import beautify_time, get_total_hours
        from utils.db_utils import vehicle_handler

        vehicle = vehicle_handler.get_vehicle_info_by_id(id=self.vid)

        rent_duration, total_sec = get_total_hours(self.start_time, self.end_time)
        if vehicle['type'] == 'bike':
            self.bill_total = 5 + int(total_sec) * 0.0002
        elif vehicle['type'] == 'scooter':
            self.bill_total = 7 + int(total_sec) * 0.0003
        self.bill_total = round(self.bill_total, 2)
        self.end_time = datetime.now().isoformat()
        self.status = 'paying'
        if self.loc_to is None:
            result = f"""
Rental ID: {self.id}
Vehicle: {vehicle['id']}-{vehicle['type']}
Start Time: {beautify_time(self.start_time)}
Start Location: {self.loc_from}
Duration: {rent_duration}
Charged amount: £{self.bill_total} 
        """
        else:
            result = f"""
Rental ID: {self.id}
Vehicle: {vehicle['type']}-{vehicle['id']}
Start Date: {beautify_time(self.start_time)}
Start Location: {self.loc_from}
End Date: {beautify_time(self.end_time)}
End Location: {self.loc_to}
Duration: {rent_duration}
Charged amount: £{self.bill_total} 
                """
        return result, self.to_dict()