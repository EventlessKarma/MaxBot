import discord
import command_funcs_extra as extra
import requests
import json


# for processing of message and hold command funcs
class TextCommands:

    def __init__(self, prefix: str, msg_in: discord.Message):

        # save command prefix and discord.Message object
        self.PREFIX = prefix
        self.msg_in = msg_in

        # remove prefix
        self.msg_in.content = self.msg_in.content[1:]

        # separate command and args
        self.msg_args = msg_in.content.split(" ")

        # command as first word
        self.command = self.msg_args.pop(0)

        # contains all maxbot commands
        self.cmds = {

            "roll": roll,
            "adv": adv,
            "dis": dis,
            "check": check,
            "stats": stats,
            "word": word,
            'help': help

        }

    # will execute the desired command
    def do(self):

        try:
            return self.cmds[self.command](self)
        except KeyError:
            return None


# general roll of dice
def roll(self: TextCommands) -> str:

    # running sum and output message over all args
    total = 0
    msg_out = []

    # loop over each argument
    for arg in self.msg_args:

        temp_r = None
        temp_msg = None

        # loop over the argument checks
        for func in extra.arg_to_roll:

            # if the check is successful it will return rolls and message, then break the loop
            try:
                temp_r, temp_msg = func(self, arg)
                break

            # runtime will be thrown if check fails
            except RuntimeError:
                continue

        # temp_r will be None if argument is not understood
        if not temp_r:
            temp_r = 0
            temp_msg = 'Nani??'

        total += temp_r
        msg_out.append(temp_msg)

    # pass list of rolls matching argument list to convert to message to return
    return extra.roll_to_code_block(self, msg_out, total)


# check command for rolling d20
def check(self: TextCommands) -> str:
    
    # get the roll and the modifier
    try:
        r, modifier = extra.general_check(self)

    # runtime error if args not understood
    except RuntimeError:
        r = 0
        modifier = 0

    # reorganising for roll_to_code_block
    self.msg_args = ["1d20", str(modifier)]

    return extra.roll_to_code_block(self, [str(r), str(modifier)], r+modifier)


# adv command for rolling d20 with advantage
def adv(self: TextCommands) -> str:

    # get the roll and the modifier
    try:
        r, modifier = extra.general_check(self, adv=True)

    # runtime error if args not understood
    except RuntimeError:
        r = [0, 0]
        modifier = 0

    # reorganise for roll_to_code_block
    self.msg_args = ["2d20", str(modifier)]

    # select larger roll for advantage
    if r[0] > r[1]:
        total = r[0] + modifier
    else:
        total = r[1] + modifier

    return extra.roll_to_code_block(self, ["{} {}".format(str(r[0]), str(r[1])), str(modifier)], total )
    

# dis command for d20 with disadvantage
def dis(self: TextCommands) -> str:

    # get roll and modifier
    try:
        r, modifier = extra.general_check(self, adv=True)

    # runtime error if args not understood
    except RuntimeError:
        r = [0, 0]
        modifier = 0

    # reorganise for roll_to_code_block
    self.msg_args = ["2d20", str(modifier)]

    # select smaller roll for disadvantage
    if r[0] < r[1]:
        total = r[0] + modifier
    else:
        total = r[1] + modifier

    return extra.roll_to_code_block(self, ["{} {}".format(str(r[0]), str(r[1])), str(modifier)], total)


# roll stats sent on website
def stats(self: TextCommands) -> str:

    # get public ip
    public_ip = requests.get('https://api.ipify.org').text

    # return the website address for the user
    return "http://{}:9999/{}".format(public_ip, self.msg_in.author.id)


# print large words command
def word(self: TextCommands) -> str:

    # each character has associated text block saved in words.json
    f = open('words.json', 'r')
    data = json.load(f)
    f.close()

    # loop over the received argument
    # loop over 3 lines for output word
    # character accessed in dictionary with data[ CHARACTER ][ LINE ]
    to_return = ''
    for i in range(3):
        for j in self.msg_in.content[5:].lower():
            to_return += data[str(j)][str(i+1)] + ' '

        to_return += '\n'

    return to_return


# command for help message
def help(self: TextCommands) -> str:

    help_msg = """
    ```css
    {{MaxBot: ' help! '}}
    
    --------------------- Commands --------------------
    Separate command and arguments with space
    commands must be preceded by {PREFIX}
    
    :roll   will roll a dice, can chain multiple arguments
            Arguments --> [ ndx ] will make n rolls of size x
                          [ x ] will roll once with dice size of x
                          [ +x ] will add a modifier of size x
    
    :check  will roll a d20 dice
            Arguments --> [ x ] will add a modifier of size x
    
    :adv    will roll a d20 with advantage
            Arguments --> [ x ] will add a modifier of size x
            
    :dis    will roll a d20 with disadvantage
            Arguments --> [ x ] will add a modifier of size x
    
    :help   displays this message
    
    IF YOU TYPE THE COMMAND/ARGS WRONG IT WILL NOT WORK
    
    thank you for your cooperation
    
    ```
    
    -------- RawSauce --------
    https://github.com/EventlessKarma/MaxBot
    
    """.format(PREFIX=self.PREFIX)

    return help_msg
