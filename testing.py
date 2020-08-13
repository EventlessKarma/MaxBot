import MaxBot
import server
import commands
import command_funcs_extra
import database


class Author:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class TestMessage:
    def __init__(self, content: str, author: Author):
        self.content = content
        self.author = author


TEST_ID = 1
TEST_NAME = "test"
PREFIX = "'"

t1 = commands.TextCommands(TestMessage("{}}roll 3d20 20 +4 -3".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()

t2 = commands.TextCommands(TestMessage("{}check".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()
t3 = commands.TextCommands(TestMessage("{}check 5".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()

t4 = commands.TextCommands(TestMessage("{}adv".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()
t5 = commands.TextCommands(TestMessage("{}adv -3".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()

t6 = commands.TextCommands(TestMessage("{}dis".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()
t7 = commands.TextCommands(TestMessage("{}dis 3".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()

t8 = commands.TextCommands(TestMessage("{}stats".format(PREFIX), Author(TEST_ID, TEST_NAME))).do()

print(t1, t2, t3, t4, t5, t6, t7, t8)








