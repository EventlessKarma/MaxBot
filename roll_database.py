import sqlite3 as sql
import datetime
import os

# RollDatabase is used to read and write to database file
# database structured with:
# Dice table --> user id, rolls, total rolls
class RollDatabase:

    def __init__(self, db_name: str = "../MaxBot_data/roll_data/" + str(datetime.date.today()) + ".db"):

        # open a database file
        # by default current day file will open
        self.conn = sql.connect(db_name)
        self.cursor = self.conn.cursor()
        return

    # dont want to save very large dice rolls, or negative ones
    def check_dice(self, dice: int):
        if dice > 100 or dice < 1:
            raise ValueError

    # will generate a table for specific dice roll
    def create_table(self, dice: int):
        
        # will throw ValueError if dice is too large
        self.check_dice(dice)

        # table created by looping dice number of times to produce enough columns
        sql_command = "CREATE TABLE d{} (user_id INTEGER,".format(dice)
        for i in range(1, dice + 1):
            sql_command += "n_{} INTEGER,".format(i)
        sql_command += "total INTEGER);"

        try:
            
            # excecute and save
            self.cursor.execute(sql_command)
            self.conn.commit()

        # failure/success determines return
        except:
            return False
        
        else:
            return True


    # will generate row for a new user in a dice table
    def new_user(self, user_id: int, dice: int):
        
        # will throw ValueError on failure
        self.check_dice(dice)

        # row created by initialising columns to 0 with user_id
        sql_command = "INSERT INTO d{} (user_id".format(dice)
        for i in range(1, dice + 1):
            sql_command += ", n_{}".format(i)
        sql_command += ", total) VALUES ({}".format(user_id)
        for i in range(dice+1):
            sql_command += ", 0"
        sql_command += ");"

        try:

            # excecute and save
            self.cursor.execute(sql_command)
            self.conn.commit() 

        # success/failure determines return
        except:       
            return False

        else:
            return True


    # returns a list/row of database file
    def get_rolls(self, user_id: int, dice: int):
        
        # if dice size invalid, return empty list
        try:
            self.check_dice(dice)
        
        except ValueError:
            return []

        # check whether the required data exists
        if not self.check_table(dice) or not self.check_user(user_id, dice):
            return [] 
        
        try:

            # excecute 
            self.cursor.execute("SELECT * FROM d{} WHERE user_id == {}".format(dice, user_id))
            row = self.cursor.fetchall()
            print(row)

        except:
            return []

        return row[0]


    # will save result of a roll
    def update_roll(self, user_id: int, dice: int, roll: int):
    
        # will throw ValueError on failure
        self.check_dice(dice)
    
        try:

            # will increase (dice table), (user row), roll and total element by one
            self.cursor.execute("UPDATE d{dice} SET n_{roll} = n_{roll} + 1, total = total + 1  WHERE user_id == {user_id}".format(user_id = user_id, roll = roll, dice = dice))
            self.conn.commit()   

        except sql.OperationalError:
            print("update_roll error")
            return False

        return True     


    # check whether a user has a row in a table
    def check_user(self, user_id: int, dice: int): 
        
        # failure will throw ValueError
        self.check_dice(dice)
    
        try:

            # attempt to fetch data for the user
            self.cursor.execute("SELECT * FROM d{dice} WHERE user_id == {user_id}".format(dice = dice, user_id = user_id))
            row = self.cursor.fetchall()

        # a failure means user does not exist in database
        except sql.OperationalError:    
            return False

        # row will be empty if no user
        if not row:
            return False
    
        # success means user exists
        return True


    # check whether a particular dice table exists
    def check_table(self, dice: int): 
        
        # failure will throw ValueError
        self.check_dice(dice)
    
        try:
            
            # attempt to find the table
            self.cursor.execute("SELECT * FROM d{}".format(dice))

        # failure if not found
        except sql.OperationalError:
            return False

        # success means table exists
        return True


    # close the connection to the database
    def close(self):
        self.conn.close()


# will return all rolls for a particular user and dice
def get_all_rolls(user_id: int, dice: int):
    
    # test to ensure dice is correct size
    test = RollDatabase()
    try:
        test.check_dice(dice)
    except ValueError:
        return []

    # temp list for storing all data for the user
    all_roll = []

    # loop over each file in databases directory
    for file in os.listdir("../MaxBot_data/roll_data/"):

        # open the database
        db = RollDatabase(os.path.join("../MaxBot_data/roll_data/",file))

        # get the rolls for the user
        temp = db.get_rolls(user_id, dice)
  
        # if there is no data, skip to next file
        if not len(temp):
            continue

        # if data is found, save in all_roll
        else:
            all_roll.append(temp)

    # loop over each set of data, and sum
    lst = []
    for i in range(len(all_roll[0])):
        temp = 0
        for j in all_roll:
            temp += j[i]
        lst.append(temp)
    
    # returns sum of all rolls in get_rolls format
    return lst