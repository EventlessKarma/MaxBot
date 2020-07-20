import sqlite3 as sql
import datetime
import os

class RollDatabase:

    def __init__(self, db_name: str = "roll_data/" + str(datetime.date.today()) + ".db"):
        self.conn = sql.connect(db_name)
        self.cursor = self.conn.cursor()
        print("Opened {}".format(db_name))
        return

    def check_dice(self, dice: int):
        if dice > 100 or dice < 1:
            raise ValueError

    def create_table(self, dice: int):
        
        self.check_dice(dice)

        sql_command = "CREATE TABLE d{} (user_id INTEGER,".format(dice)
        for i in range(1, dice + 1):
            sql_command += "n_{} INTEGER,".format(i)
        sql_command += "total INTEGER);"

        self.cursor.execute(sql_command)
        self.conn.commit()
    
        return True

    def new_user(self, user_id: int, dice: int):
    
        self.check_dice(dice)
    
        sql_command = "INSERT INTO d{} (user_id".format(dice)
        for i in range(1, dice + 1):
            sql_command += ", n_{}".format(i)
        sql_command += ", total) VALUES ({}".format(user_id)
        for i in range(dice+1):
            sql_command += ", 0"
        sql_command += ");"

        self.cursor.execute(sql_command)
        self.conn.commit()        

    def get_rolls(self, user_id: int, dice: int):
    
        try:
            self.check_dice(dice)
        except ValueError:
            return []

        if not self.check_table(dice) or not self.check_user(user_id, dice):
            return [] 
    
        self.cursor.execute("SELECT * FROM d{} WHERE user_id == {}".format(dice, user_id))
        row = self.cursor.fetchall()
        print(row)
    
        return row[0]

    def update_roll(self, user_id: int, dice: int, roll: int):
    
        self.check_dice(dice)
    
        try:
            self.cursor.execute("UPDATE d{dice} SET n_{roll} = n_{roll} + 1, total = total + 1  WHERE user_id == {user_id}".format(user_id = user_id, roll = roll, dice = dice))
            self.conn.commit()   
        except sql.OperationalError:
           return False

        return True     

    def check_user(self, user_id: int, dice: int): 
    
        self.check_dice(dice)
    
        try:
            self.cursor.execute("SELECT * FROM d{dice} WHERE user_id == {user_id}".format(dice = dice, user_id = user_id))
            ret = self.cursor.fetchall()
        except sql.OperationalError:    
            return False
    
        if not ret:

            return False
    
        return True

    def check_table(self, dice: int): 
    
        self.check_dice(dice)
    
        try:
            self.cursor.execute("SELECT * FROM d{}".format(dice))
        except sql.OperationalError:
            return False

        return True

    def close(self):
        self.conn.close()


def get_all_rolls(user_id: int, dice: int):
    
    test = RollDatabase()
    try:
        test.check_dice(dice)
    except ValueError:
        return []


    all_roll = []
    for file in os.listdir("roll_data/"):
        db = RollDatabase(os.path.join("roll_data/",file))
        temp = db.get_rolls(user_id, dice)
        if not len(temp):
            continue
        else:
            all_roll.append(temp)

    lst = []
    for i in range(len(all_roll[0])):
        temp = 0
        for j in all_roll:
            temp += j[i]
        lst.append(temp)
    
    return lst