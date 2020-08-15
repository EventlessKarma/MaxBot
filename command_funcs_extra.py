import numpy as np
import database
import matplotlib.pyplot as plt
import datetime
import math
import random


# old function used to generate roll graphs
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
        date = datetime.date.today()
        db = database.RollDatabase()
        rolls = db.get_rolls(user_id, dice)
    else:
        rolls = database.get_all_rolls(user_id, dice)

    # make x coords
    x = []
    for i in range(1, dice + 1):
        x.append(i)
    y = rolls[1:-1]

    # plot bar graph
    plt.bar(x, y, width=1, color='green', edgecolor='black')
    yint = range(min(y), math.ceil(max(y)) + 1)
    plt.yticks(yint)
    xint = range(1, dice + 1)
    plt.xticks(xint)
    plt.title(user_name + " d" + str(dice) + " rolls - " + str(date))
    plt.ylabel("Frequency")
    plt.xlabel("Roll")

    # save image to send
    image_name = "../MaxBot_data/temp_stat.png"
    plt.savefig(image_name)
    plt.clf()

    return image_name


# stole this to get a random line from file
def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num): continue
        line = aline
    return line


# converts roll output and arguments into more readable form
def roll_to_code_block(self, roll_out: list, total: int) -> str:

    # output code block uses highlight.js

    # start code block with css format
    msg = "```css\n"
    msg += "{" + self.msg_in.author.name.replace(" ", "") + ": ' "  # username
    msg += "{} ".format(self.command)  # users command

    # print all users arguments
    for i in self.msg_args:
        msg += i + " "
    msg += "'}\n"

    # print arguments and responses
    for i, j in zip(self.msg_args, roll_out):
        msg += ":{} {}\n".format(i, j)

    # finally print total roll
    msg += ":Total {}\n".format(str(total))

    # end code block
    msg += "```"

    return msg


def general_check(self, adv: bool = False) -> (int, int):

    # if no modifier arg is found set it to 0
    if not len(self.msg_args):
        modifier = 0

    else:
        
        # try to turn modifier arg into int
        try: 
            modifier = int(self.msg_args[0])
        except ValueError:
            
            # failure returns the roll as 0
            raise RuntimeError("Invalid modifier argument for general_check")

    # for normal check roll a d20
    if not adv:
        roll = np.random.randint(20) + 1
        database.update_database(self.msg_in.author.id, 20, [roll])
        return roll, modifier

    # for adv/disadv roll 2d20
    else:
        roll = np.random.randint(20, size=2)
        for i in range(2):
            roll[i] += 1
            
        database.update_database(self.msg_in.author.id, 20, [roll[0]])
        database.update_database(self.msg_in.author.id, 20, [roll[1]])
            
        return roll, modifier


# for checking roll arguments of ndx form
def d_check(self, arg: str) -> (int, str):
    
    # find position of d
    d_pos = arg.rfind('d')

    if d_pos == -1:
        raise RuntimeError('Inappropriate argument for d_check')

    try:

        # get rolls and dice from arguments
        dice = int(arg[d_pos + 1:])
        n_rolls = int(arg[:d_pos])

    except ValueError:
        raise RuntimeError('Inappropriate argument for d_check')

    # stop scott rolling a trillion times at once
    if n_rolls > 100:
        return 0, "Too many rolls at once"

    # numpy returns array of random numbers from [0] to [dice-1]
    rands = np.random.randint(dice, size=n_rolls)

    temp_msg = ""
    temp_total = 0

    # loop over all numbers generated
    for r in rands:
        # plus one as generated starts from 0
        r += 1
        database.update_database(self.msg_in.author.id, dice, [r])
        temp_msg += str(r) + " "
        temp_total += r

    # return total of all rolls and string of individual rolls
    return temp_total, temp_msg


# for checking roll args for modifier
def m_check(self, arg: str) -> (int, str):

    # search for instance of +/- to signal a modifier
    if arg.rfind('+') == -1 and arg.rfind('-') == -1:
        raise RuntimeError('Inappropriate argument for m_check')

    try:

        # convert the argument into integer for modifier
        mod = int(arg)
        return mod, str(mod)

    except ValueError:
        raise RuntimeError('Inappropriate argument for m_check')


# for checking roll args for single roll
def r_check(self, arg: str) -> (int, str):

    # if the arg can be converted to integer it is one roll
    try:
        dice = int(arg)
        temp_r = np.random.randint(dice) + 1
        database.update_database(self.msg_in.author.id, dice, [temp_r])
        return temp_r, str(temp_r)

    except ValueError:
        raise RuntimeError('Inappropriate argument for r_check')


# group the roll checks for easy access
arg_to_roll = [

    d_check,
    m_check,
    r_check

]
