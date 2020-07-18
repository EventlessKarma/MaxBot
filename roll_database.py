import sqlite3 as sql
import datetime
import os

today = datetime.date.today()
database = "roll_data/" + str(today) + ".db"
print(database)
#db = "file:{}?mode=rwc".format(database)
#conn = sql.connect(db)
conn = sql.connect(database)
cursor = conn.cursor()


def check_dice(dice: int):
    
    if dice > 100 or dice < 1:
        print("dice size invalid")
        return False
    else:
        return True

    

def create_table(dice: int):
    
    if check_dice(dice):
        pass
    else:
        return False
    
    sql_command = "CREATE TABLE d{} (user_id INTEGER,".format(dice)
    
    for i in range(1, dice + 1):
        sql_command += "n_{} INTEGER,".format(i)
        
    sql_command += "total INTEGER);"
    
    cursor.execute(sql_command)
    
    conn.commit()
    
    return True


def new_user(user_id: int, dice: int):
    
    if check_dice(dice):
        pass
    else:
        return False
    
    sql_command = "INSERT INTO d{} (user_id".format(dice)
    
    for i in range(1, dice + 1):
        sql_command += ", n_{}".format(i)

    sql_command += ", total) VALUES ({}".format(user_id)

    for i in range(dice+1):
        sql_command += ", 0"
        
    sql_command += ");"
    
    cursor.execute(sql_command)
    
    conn.commit()
        

def get_rolls(user_id: int, dice: int):
    
    if check_dice(dice) == False:
        return False
    
    try:
        cursor.execute("SELECT * FROM d{} WHERE user_id == {}".format(dice, user_id))
        row = cursor.fetchall()
    except:

        return False
    
    return row


def get_all_rolls(user_id: int, dice: int):
    
    if check_dice(dice) == False:
        return False
    
    conn.close()
    
    all_roll = []
    for file in os.listdir("roll_data/"):
        print(file)
        conn = sql.connect(os.path.join("roll_data/", file))                       
        cursor = conn.cursor()
        if check_table(dice) and check_user(user_id, dice):
            all_roll.append(get_rolls(user_id, dice)[0])
        conn.close()

    print(all_roll)

    lst = []
    for i in range(len(all_roll[0])):
        temp = 0
        for j in all_roll:
            temp += j[i]
        lst.append(temp)

    conn = sql.connect(database)
    cursor = conn.cursor()
    
    return lst
    
def update_roll(user_id: int, dice: int, roll: int):
    
    if check_dice(dice) == False:
        return False
    
    try:
        cursor.execute("UPDATE d{dice} SET n_{roll} = n_{roll} + 1, total = total + 1  WHERE user_id == {user_id}".format(user_id = user_id, roll = roll, dice = dice))
        conn.commit()   
        
    except sql.OperationalError:

        return False

    
    return True     
    
    
def check_user(user_id: int, dice: int): 
    
    if check_dice(dice) == False:
        return False
    
    try:
    
        cursor.execute("SELECT * FROM d{dice} WHERE user_id == {user_id}".format(dice = dice, user_id = user_id))
        ret = cursor.fetchall()
        
    except sql.OperationalError:
        
        return False
    
    if not ret:

        return False
    
    
    return True
    
    
def check_table(dice: int): 
    
    if check_dice(dice) == False:
        return False
    
    try:
    
        cursor.execute("SELECT * FROM d{}".format(dice))
    
    except sql.OperationalError:

        return False

    return True
    
    
    
def test(user_id: int):

    cursor.execute("SELECT * FROM d20 WHERE user_id == {}".format(user_id))
    fet = cursor.fetchall()
    return fet










    