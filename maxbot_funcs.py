import roll_database as rdb
import numpy as np
import matplotlib.pyplot as plt
import math
import random

def check_dice(dice: int):

    if dice > 100 or dice < 1:
        raise ValueError

def update_database(user_id: int, dice: int, roll: int):

    # open database
    db = rdb.RollDatabase()

    try:

        # check dice table
        if db.check_table(dice) == False:
            db.create_table(dice)
    
        # check user 
        if db.check_user(user_id, dice) == False:
            db.new_user(user_id, dice)
            
        # update roll
        db.update_roll(user_id, dice, roll)
        
    except ValueError:

        # bad dice size will throw and not update database
        return False
 
    except:
        
        print("Error updating database")
        return False

    return True


def bot_roll(user_id, args):
    
    # running total of roll
    total = 0

    # answer/response for each argument
    msg= []
    
    # handle each user input
    for arg in args:
        
        error_msg = arg + " Nani??? "
        
        # ----------------------------------------------------------------------------------
        # look for arguments of form 1d4

        # find position of d
        d_pos = arg.rfind('d')

        # if found try to get number of rolls and dice type
        if d_pos != -1:
            try:

                dice = int(arg[d_pos+1:]) 
                n_rolls = int(arg[:d_pos])
            
            except:

                # failure will skip argument
                msg.append(error_msg)
                continue
            
            # cant have users asking for a billion rolls
            if n_rolls > 100:
                msg.append("Too many rolls at once")
                continue
            
            # save each roll outcome
            temp_msg = ""

            # generate array of random numbers
            rands = np.random.randint(dice, size=n_rolls)
            
            # loop over numbers to add to total and update database
            for r in rands:
                r += 1
                temp_msg += str(r) + " "
                update_database(user_id, dice, r)
                total += r
            
            msg.append(temp_msg)
            continue

        # ----------------------------------------------------------------------------------
        # MODIFIER CHECK

        # check for a "+"" char identifies a modifier
        if arg.rfind('+') != -1 or arg.rfind('-') != -1:

            # attempt to turn argument into number
            try:

                total += int(arg)
                msg.append(arg)
                continue

            except:

                msg.append(error_msg)
                continue
        
        # ----------------------------------------------------------------------------------
        # SINGLE NUMBER CHECK

        # try to turn argument into number and generate roll
        try:

            temp_roll = np.random.randint(int(arg)) + 1

        except:

            # failure skips to next arg
            msg.append(error_msg)
            continue

        # update total, database
        total += temp_roll
        msg.append(str(temp_roll))
        update_database(user_id, int(arg), temp_roll)
        continue

        # ----------------------------------------------------------------------------------

        
    return total, msg 


def checks_roll(user_id: int, args, adv: bool = False):

    # if no modifier arg is found set it to 0
    if len(args) == 1:
        modifier = 0

    else:
        
        # try to turn modifier arg into int
        try: 
            modifier = int(args[1])
        except:
            
            # failure returns the roll as 0
            return 0, modifier

    # for normal check roll a d20
    if not adv:
        roll = np.random.randint(20) + 1
        return roll, modifier

    # for adv/disadv roll 2d20
    else:
        roll = np.random.randint(20, size=2)
        for i in range(2):
            roll[i] += 1
            update_database(user_id, 20, roll[i])
            
        return roll, modifier


def get_stats(user_name: str, user_id: int, args, date: str = "today"):
    
    # get dice and check size
    try:
        dice = int(args[1])
    except:
        return
    if dice > 100 or dice < 1:
        return

    # for general cases of different days
    if date == "today":
        db = rdb.RollDatabase()
        rolls = db.get_rolls(user_id, dice)
    else:
        rolls = rdb.get_all_rolls(user_id, dice)
    
    # make x coords
    x = []
    for i in range(1, dice+1):
        x.append(i)
    y = rolls[1:-1]
            
    # plot bar graph
    plt.bar(x, y, width = 1, color='green', edgecolor='black')
    yint = range(min(y), math.ceil(max(y))+1)
    plt.yticks(yint)
    xint = range(1, dice+1)
    plt.xticks(xint)
    plt.title(user_name + " d" + str(dice) + " rolls")
    plt.ylabel("Frequency")
    plt.xlabel("Roll")
            
    # save image to send
    image_name = "temp_stat.png"
    plt.savefig(image_name)
    plt.clf()

    return image_name


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
      if random.randrange(num): continue
      line = aline
    return line


def help():
    pass