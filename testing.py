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

# database_json.update_from_history()

db_json = database_json.Database()
db_json.update(1, "testname", 20, 1, datetime.date(2020, 8, 13))
print(db_json.get(1, datetime.date(2020, 8, 13), 20))
del db_json
