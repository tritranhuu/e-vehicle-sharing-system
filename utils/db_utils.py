from database.db_handler import DBHandler
from database.entity_db_handlers import *


DB_PATH = "database/EVehicle.db"
db_handler = DBHandler(DB_PATH)

user_handler = UserHandler(db_handler)

rental_handler = RentalHandler(db_handler)

vehicle_handler = VehicleHandler(db_handler)

report_handler = ReportHandler(db_handler)

topup_handler = TopupHandler(db_handler)