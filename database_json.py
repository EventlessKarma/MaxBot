import json
import datetime
import os
import numpy as np
import database
import sqlite3


class Database:
    def __init__(self, db_name='database.json'):

        self.db_name = db_name
        self.f = open(self.db_name)
        self.data = json.load(self.f)
        self.day = datetime.date.today().strftime('%m/%d/%Y')

    def check_id(self, user_id):
        self.data.setdefault(user_id, {})

    def check_name(self, user_name: str, user_id):
        self.data[user_id].setdefault('name', user_name)

    def check_day(self, user_id: str, day=datetime.date.today().strftime('%m/%d/%Y')):
        self.data[user_id].setdefault(day, {})

    def check_dice(self, user_id: str, dice: int, day=datetime.date.today().strftime('%m/%d/%Y')):
        self.data[user_id][day].setdefault(str(dice), np.zeros(dice).tolist())

    def update(self, user_id: int, user_name: str, dice: int, roll: int, date=datetime.date.today()):
        USER_ID = str(user_id)
        USER_NAME = str(user_name)
        day = date.strftime('%m/%d/%Y')

        self.check_id(USER_ID)
        self.check_name(USER_NAME, USER_ID)
        self.check_day(USER_ID, day)
        self.check_dice(USER_ID, dice, day)

        self.data[USER_ID][day][str(dice)][roll - 1] += 1

    def get(self, user_id: int, date: datetime.date, dice: int):

        return self.data[str(user_id)][date.strftime('%m/%d/%Y')][str(dice)]

    def __del__(self):
        json.dump(self.data, self.f, sort_keys=True, indent=4, separators=(',', ': '))
        self.f.close()


def update_from_history():

    json_db = Database()

    for filename in os.listdir('roll_data/'):

        a = filename[:-3]
        # yr, mon, day
        b = a.split('-')
        b = [int(n) for n in b]

        day = datetime.datetime(b[0], b[1], b[2])

        conn = sqlite3.connect('roll_data/{}'.format(filename))
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()

        if not table_names:
            continue

        for table in table_names:
            table = table[0]
            print('working with table {}'.format(table))
            table_num = int(table[1:])

            cursor.execute("SELECT * FROM {}".format(table))
            all = cursor.fetchall()
            print(all)

            for line in all:
                rolls = line[1:-1]
                print(rolls)

                for roll, count in enumerate(rolls):
                    for i in range(count):
                        pass
                        # json_db.update(line[0], "UNKNOWN", table_num, roll + 1, day)

    del json_db






