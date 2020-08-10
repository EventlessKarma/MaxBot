import numpy as np
import request_rolls
import commands


def roll_to_code_block(self: commands.TextCommands, roll_out: list, total: int) -> str:

    # start code block
    msg = "```css\n"
    msg += "{" + self.msg_in.author.name.replace(" ", "") + ": ' "  # username

    # print full user command
    for i in self.msg_args:
        msg += i + " "
    msg += "'}\n"

    # print arguments and responses
    for i, j in zip(self.msg_args[1:], roll_out):
        msg += ":{} {}\n".format(i, j)

    # finally print total roll
    msg += ":Total {}\n".format(str(total))

    # end code block
    msg += "```"

    return msg


def general_check(self: commands.TextCommands, adv: bool = False) -> (int, int):

    # if no modifier arg is found set it to 0
    if len(self.msg_args):
        modifier = 0

    else:
        
        # try to turn modifier arg into int
        try: 
            modifier = int(self.msg_args[1])
        except ValueError:
            
            # failure returns the roll as 0
            raise RuntimeError("Invalid modifier argument for general_check")

    # for normal check roll a d20
    if not adv:
        roll = np.random.randint(20) + 1
        request_rolls.update_rolls(self.msg_in.author.id, 20, str(roll))
        return roll, modifier

    # for adv/disadv roll 2d20
    else:
        roll = np.random.randint(20, size=2)
        for i in range(2):
            roll[i] += 1
            
        request_rolls.update_rolls(self.msg_in.author.id, 20, "{} {}".format(roll[0], roll[1]))
            
        return roll, modifier


def d_check(self: commands.TextCommands, arg: str) -> (int, str):
    
    # find position of d
    d_pos = arg.rfind('d')

    if d_pos == -1:
        raise RuntimeError('Inappropriate argument for d_check')

    try:

        dice = int(arg[d_pos + 1:])
        n_rolls = int(arg[:d_pos])

    except ValueError:
        raise RuntimeError('Inappropriate argument for d_check')

    if n_rolls > 100:
        return 0, "Too many rolls at once"

    rands = np.random.randint(dice, size=n_rolls)

    temp_msg = str(rands[0] + 1)
    temp_total = rands[0] + 1

    for r in rands[1:]:
        r += 1
        temp_msg += " " + str(r)
        temp_total += r
    
    request_rolls.update_rolls(self.msg_in.author.id, dice, temp_msg)

    return temp_total, temp_msg


def m_check(self: commands.TextCommands, arg: str) -> (int, str):
    
    if arg.rfind('+') == -1 and arg.rfind('-') == -1:
        raise RuntimeError('Inappropriate argument for m_check')

    try:
        
        mod = int(arg)
        return mod, str(mod)

    except ValueError:
        raise RuntimeError('Inappropriate argument for m_check')


def r_check(self: commands.TextCommands, arg: str) -> (int, str):
    
    try:
        dice = int(arg)
        temp_r = np.random.randint(dice) + 1
        request_rolls.update_rolls(self.msg_in.author.id, dice, str(temp_r))
        return temp_r, str(temp_r)

    except ValueError:
        raise RuntimeError('Inappropriate argument for r_check')


arg_to_roll = [

    d_check,
    m_check,
    r_check

]