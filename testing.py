import MaxBot
import server
import commands
import command_funcs_extra
import database
import datetime
import database_json
import numpy as np

"""
for testing modules and functions without starting maxbot
"""


# imitate discord.Message class
class Author:
    def __init__(self, user_id: int, name: str):
        self.id = user_id
        self.name = name


class TestMessage:
    def __init__(self, content: str, author: Author):
        self.content = content
        self.author = author


# rolls will be saved under these details
TEST_ID = 1
TEST_NAME = "test"
PREFIX = "'"

t1 = commands.TextCommands(PREFIX, TestMessage("{}roll 3d20 20 +4 -3".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()

t2 = commands.TextCommands(PREFIX, TestMessage("{}check".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()
t3 = commands.TextCommands(PREFIX, TestMessage("{}check 5".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()

t4 = commands.TextCommands(PREFIX, TestMessage("{}adv".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()
t5 = commands.TextCommands(PREFIX, TestMessage("{}adv -3".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()

t6 = commands.TextCommands(PREFIX, TestMessage("{}dis".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()
t7 = commands.TextCommands(PREFIX, TestMessage("{}dis 3".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()

t8 = commands.TextCommands(PREFIX, TestMessage("{}stats".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()

print(t1, t2, t3, t4, t5, t6, t7, t8)


db = database_json.Database()
date = datetime.date.today()
rand = np.random.randint(20, size=100)
print(db.data)
for r in rand:
    db.save(1, "na", 20, r)
    db.save(1, 'df', 21, r)
    db.save(1, 'dfdf', 22, r)
    db.save(2, 'wow', 30, r)
    db.save(3, 'odo', 23, r)

database_json.update_from_history()


