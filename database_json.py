import json
import datetime
import os
import numpy as np
import database


class Database:
    def __init__(self, db_name='user_names.json'):

        self.db_name = db_name

        with open(self.db_name, 'r') as f:
            self.data = json.load(f)
            self.day = datetime.date.today().strftime('%m/%d/%Y')

    def check_id(self, user_id):
        self.data.setdefault(user_id, {})

    def check_name(self, user_name: str, user_id):
        self.data[user_id].setdefault('name', user_name)

    def check_day(self, user_id: str):
        self.data[user_id].setdefault(self.day, {})

    def check_dice(self, user_id: str, dice: int):
        self.data[user_id][self.day].setdefault(str(dice), np.zeros(dice).tolist())

    def save(self, user_id: int, user_name: str, dice: int, roll: int):
        USER_ID = str(user_id)
        USER_NAME = str(user_name)

        self.check_id(USER_ID)
        self.check_name(USER_NAME, USER_ID)
        self.check_day(USER_ID)
        self.check_dice(USER_ID, dice)

        self.data[USER_ID][self.day][str(dice)][roll - 1] += 1

        with open(self.db_name, 'w') as outfile:
            json.dump(self.data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    def get(self, user_id: int, date: datetime.date, dice: int):

        return self.data[str(user_id)][date.strftime('%m/%d/%Y')][str(dice)]



def update_from_history():
    for filename in os.listdir('roll_data/'):
        a = filename[:-3]
        b = a.split('-')

