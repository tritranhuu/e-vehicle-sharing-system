import sqlite3
import random
from tqdm import trange
from datetime import datetime, timedelta
from random import randrange
from datetime import timedelta
from utils.db_utils import *

# def random_date(start, end):
#     """
#     This function will return a random datetime between two datetime
#     objects.
#     """
#     delta = end - start
#     int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
#     random_second = randrange(int_delta)
#     result = start + timedelta(seconds=random_second+0.1)
#     return result
#
# d1 = datetime.strptime('1/1/1980', '%m/%d/%Y')
# d2 = datetime.strptime('1/1/2010', '%m/%d/%Y')
#
# print(random_date(d1, d2))
#
# db = sqlite3.connect("../database/EVehicle.db")
#
# cursor = db.cursor()
#
locations = [line.strip() for line in open("./data/locations.txt").readlines()]
# usernames = [line.strip() for line in open("../data/usernames.txt").readlines() if len(line.strip())>5]
# passwords = [line.strip() for line in open("../data/usernames.txt").readlines()]
# def create_random_vehicles():
#     v_type = random.choice(["bike", "scooter"])
#     location = random.choice(locations)
#     battery = random.randint(0, 100)
#     status = random.choice(['available', 'available', 'available']*2 + ['defective'])
#     query = f"""
#         INSERT INTO Vehicles
#         ('type', 'location', 'battery', 'status')
#         VALUES ('{v_type}', "{location}", {battery}, '{status}')
#     """
#     cursor.execute(query)
#     db.commit()
#
# def create_random_users():
#     username = random.choice(usernames)
#     usernames.remove(username)
#     password = random.choice(usernames)
#     dob = random_date(d1, d2).strftime('%m/%d/%y')
#     phone = "".join([str(random.randint(0, 10)) for _ in range(10)])
#     balance = round(random.random()*1000, 2)
#     query = f"""
#         INSERT INTO Users
#         ('username', 'password', 'dob', 'phone', 'balance', 'role', 'status')
#         VALUES ('{username}', '{password}', '{dob}', '{phone}', {balance}, 'customer', 'active')
#     """
#     cursor.execute(query)
#     db.commit()
#
# def create_rental():
#     uid = random.randint(2, 2100)
#     vid = random.randint(1, 9000)
#
#     loc_from = random.choice(locations)
#     loc_to = random.choice(locations)
#
#     d1 = datetime.strptime('1/1/2012', '%m/%d/%Y')
#     d2 = datetime.strptime('10/16/2023', '%m/%d/%Y')
#
#     end_time = random_date(d1, d2)
#     duration = timedelta(seconds=random.randint(3600, 3600*100))
#     start_time = end_time - duration
#
#     bill_total = duration.total_seconds()*random.choice([0.0001, 0.0002, 0.0003, 0.0004])
#     status = random.choice(['done', 'paying'])
#     query = f"""
#             INSERT INTO Rentals
#             ('uid', 'vid', 'starttime', 'endtime', 'loc_from', 'loc_to', 'billtotal','status')
#             VALUES ('{uid}', '{vid}', '{start_time.isoformat()}', '{end_time.isoformat()}', "{loc_from}", "{loc_to}", {bill_total}, '{status}')
#         """
#     cursor.execute(query)
#     db.commit()
#
# for i in trange(11200):
#     create_random_vehicles()
#
# for i in trange(15000):
#     create_random_users()
#
# for i in trange(6000):
#     create_rental()

uid_list = list(range(10, 15000))
vid_list = list(range(10, 11000))
for i in trange(3436):
    uid = uid_list.pop(random.randint(0, len(uid_list)-1))
    vid = vid_list.pop(random.randint(0, len(vid_list)-1))
    loc = random.choice(locations)
    rental_handler.create_rental(uid=uid, vid=vid, loc_from=loc)
    vehicle_handler.update_vehicle_by_id(vid, fields={"location": loc, "status": "unavailable"})