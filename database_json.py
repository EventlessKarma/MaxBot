import json
import datetime
import os
import numpy as np


class Database:
    def __init__(self, db_name='database.json'):

        with open(db_name) as f:
            self.data = json.load(f)

    def check_id(self, user_id):
        USER_ID = str(user_id)
        self.data.setdefault(USER_ID,[{}])

    def check_name(self, user_name: str, user_id):
        self.data[user_id].setdefault('name', [user_name])

    def check_day(self, user_id: str):
        self.data[user_id].setdefault(datetime.date.today(), [{}])

    def check_dice(self, user_id: str, dice: int):
        self.data[user_id][datetime.date.today()].setdefault(str(dice), [np.zeros(dice)])

    def save(self, user_id: int, user_name: str, dice: int, roll: int):
        USER_ID = str(user_id)
        USER_NAME = str(user_name)

        self.check_id(USER_ID)
        self.check_name(USER_NAME, USER_ID)
        self.check_day(USER_ID)
        self.check_dice(USER_ID, dice)

        self.data[USER_ID][datetime.date.today()][str(dice)][roll - 1] += 1

    def get(self, user_id: int, date: datetime.date, dice: int):
        try:
            return self.data[str(user_id)][date][dice]
        except KeyError:
            return np.zeroes(dice)


