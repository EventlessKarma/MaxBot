import discord
import command_funcs_extra as extra
import requests
import json


class TextCommands:

    def __init__(self, msg_in: discord.Message):

        self.msg_in = msg_in

        # remove prefix
        self.msg_in.content = self.msg_in.content[1:]

        # separate command and args
        self.msg_args = msg_in.content.split(" ")

        # command as first word
        self.command = self.msg_args.pop(0)

        self.cmds = {

            "roll": roll,
            "adv": adv,
            "dis": dis,
            "check": check,
            "stats": stats,
            "word": word,
            'help': help

        }

    def do(self):

        try:
            return self.cmds[self.command](self)
        except KeyError:
            return None


def roll(self: TextCommands) -> str:
    
    total = 0
    msg_out = []

    # loop over each argument
    for arg in self.msg_args:

        temp_r = None
        temp_msg = None

        # loop over the argument checks
        for func in extra.arg_to_roll:
            try:
                temp_r, temp_msg = func(self, arg)
                break
            except RuntimeError:
                continue

        if not temp_r:
            temp_r = 0
            temp_msg = 'Nani??'

        total += temp_r
        msg_out.append(temp_msg)

    return extra.roll_to_code_block(self, msg_out, total)


def check(self: TextCommands) -> str:
    
    # get the roll and the modifier
    try:
        r, modifier = extra.general_check(self)

    except RuntimeError:
        r = 0
        modifier = 0

    self.msg_args = ["1d20", str(modifier)]

    return extra.roll_to_code_block(self, [str(r), str(modifier)], r+modifier)


def adv(self: TextCommands) -> str:
    
    try:
        r, modifier = extra.general_check(self, adv=True)

    except RuntimeError:
        r = [0, 0]
        modifier = 0

    self.msg_args = ["2d20", str(modifier)]

    if r[0] > r[1]:
        total = r[0] + modifier
    else:
        total = r[1] + modifier

    return extra.roll_to_code_block(self, ["{} {}".format(str(r[0]), str(r[1])), str(modifier)], total )
    

def dis(self: TextCommands) -> str:

    try:
        r, modifier = extra.general_check(self, adv=True)

    except RuntimeError:
        r = [0, 0]
        modifier = 0

    self.msg_args = ["2d20", str(modifier)]

    if r[0] < r[1]:
        total = r[0] + modifier
    else:
        total = r[1] + modifier

    return extra.roll_to_code_block(self, ["{} {}".format(str(r[0]), str(r[1])), str(modifier)], total)


def stats(self: TextCommands) -> str:
    public_ip = requests.get('https://api.ipify.org').text
    return "http://{}:9999/{}".format(public_ip, self.msg_in.author.id)


def word(self: TextCommands) -> str:

    f = open('words.json', 'r')
    data = json.load(f)
    f.close()

    to_return = ''
    for i in range(3):
        for j in self.msg_in.content[5:].lower():
            to_return += data[str(j)][str(i+1)] + ' '

        to_return += '\n'

    return to_return


def help(self: TextCommands) -> str:
    help_msg = """
    ```css
    {MaxBot: ' help! '}
    :Raw Sauce https://github.com/EventlessKarma/MaxBot
    
    --------------------- Commands --------------------
    Separate command and arguments with space
    
    :roll   will roll a dice of sides up to 100, can chain multiple arguments
            Arguments --> [ ndx ] where n is number of rolls and x is dice size
                          [ x ] where x is dice size
                          [ +x ] where x is a number will add modifier
    
    :check  will roll a d20 dice
            Arguments --> [ x ] where x is the modifier
    
    :adv    will roll a d20 with advantage
            Arguments --> [ x ] where x is the modifier
            
    :dis    will roll a d20 with disadvantage
            Arguments --> [ x ] where x is the modifier
    
    :help   displays this message
    
    IF YOU TYPE THE COMMAND/ARGS WRONG IT WILL NOT WORK
    
    thank you for your cooperation
    
    ```
    """

    return help_msg