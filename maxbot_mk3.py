import discord
from discord.ext import commands
import roll_database as rdb
import numpy as np
import matplotlib.pyplot as plt
import os
import math

plt.style.use('Solarize_Light2')
global db
db = rdb.RollDatabase()

def roll_dice(dice: int):
    return np.random.randint(dice) + 1


def update_database(user_id: int, dice: int, roll: int):
    
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
        print("Invalid dice size")
        return False
    else:
        print("Error updating database")
    
    return True
    

def bot_roll(user_id, args):
    
    total = 0
    msg= []
    
    for arg in args:
        
        error_msg = arg + " Nani??? "
        
        # FOR ARG WITH FORM 3d6
        d_pos = arg.rfind('d')
        if d_pos != -1:
            try:
                dice_type = int(arg[d_pos+1:]) 
                n_rolls = int(arg[:d_pos])
            except:
                return -1, error_msg
            if n_rolls > 100:
                return -1, arg + " Too many rolls at once"
            temp_sum = 0
            temp_msg = ""
            for i in range(n_rolls):                    
                temp_roll = roll_dice(dice_type)
                temp_msg += str(temp_roll) + " "
                update_database(user_id, dice_type, temp_roll)
                temp_sum += temp_roll
            total += temp_sum
            msg.append(temp_msg)
            continue
        
        # MODIFIER CHECK
        if arg.rfind('+') != -1:
            try:
                total += int(arg[1:])
                msg.append("+" + arg[1:])
                continue
            except:
                return -1, error_msg
            
        if arg.rfind('-') != -1:
            try:
                total -= int(arg[1:])
                msg.append("-" + arg[1:])
                continue
            except:
                return -1, error_msg
    
        # SINGLE NUMBER CHECK
        try:
            temp_roll = roll_dice(int(arg))
            total += temp_roll
            msg.append(str(temp_roll))
            
            update_database(user_id, int(arg), temp_roll)
            
            continue
        except:
            return -1, error_msg
        
    return total, msg 
    
    
    
class MyClient(discord.Client):
    async def on_ready(self):
        print('Connected!')
        print('Username: {0.name}\nID: {0.id}\n'.format(self.user))

    async def on_message(self, message):
        
        prefix = "'"
        args = message.content.split(" ")
        
        if not message.author.id == self.user.id:
            print('Message from {0.author}:\n {0.content}'.format(message))
            
        if message.author.id == 469948694863544320:
            
            if np.random.randint(2):
                await message.channel.send("Yes")
            else:
                await message.channel.send("No")
                
            return
        
        if message.content.startswith(prefix + "shutdown"):
            if message.author.id == 198783211776638976:
                await message.delete()
                await self.logout()
                await self.close()
        
        
        if args[0] == prefix + "roll":
            
            roll, roll_msg = bot_roll(message.author.id, args[1:])
            
            msg = "```css\n"
            msg += "{" + message.author.name.replace(" ", "") + ": ' "
            for i in args[1:]:
                msg += i + " "
            msg += "'}\n"    
            
            if roll == -1:
                msg += ":" + roll_msg + "```"
                await message.channel.send(msg)
                await message.delete()
                return
            
            for i in range(len(args[1:])):
                msg += ":" + args[i+1] + " " + roll_msg[i] + "\n"
            
            msg += ":Total " + str(roll) + "\n"
            
            msg += "```"
            
            await message.channel.send(msg)
            await message.delete()
            return
        
        
        if args[0] == prefix + "check":
            
            if len(args) == 1:
                modifyer = 0
                sign = "+"
                
            else:
            
                try: 
                    modifyer = int(args[1])
                    if modifyer > -1:
                       sign = "+"
                    else:
                        sign = "-"
                except:
                    return
            
            roll = roll_dice(20)
            update_database(message.author.id, 20, roll)
            
            msg = "```css\n"
            msg += "{" + message.author.name.replace(" ", "") + ": ' 1d20 " + sign + " " + str(abs(modifyer)) + " '}\n"
            msg += ":20 " + str(roll) + "\n"
            msg += ":" + sign + str(abs(modifyer)) + " " + sign + str(abs(modifyer)) + "\n"
            msg += ":Total " + str(roll + modifyer) + "\n"
            msg += "```"
            await message.channel.send(msg)
            await message.delete()
            
            
        if args[0] == prefix + "checka":
            
            if len(args) == 1:
                modifyer = 0
                sign = "+"
                
            else:
            
                try: 
                    modifyer = int(args[1])
                    if modifyer > -1:
                       sign = "+"
                    else:
                        sign = "-"
                except:
                    return
                
            roll_1 = roll_dice(20)
            roll_2 = roll_dice(20)
            update_database(message.author.id, 20, roll_1)
            update_database(message.author.id, 20, roll_2)
            
            if roll_1 > roll_2:
                roll = roll_1
            else:
                roll = roll_2
            
            msg = "```css\n"
            msg += "{" + message.author.name + ": ' 1d20 " + sign + " " + str(abs(modifyer)) + " with advantage'}\n"
            msg += ":20 " + str(roll_1) + " " + str(roll_2) + "\n"
            msg += ":" + sign + str(abs(modifyer)) + " " + sign + str(abs(modifyer)) + "\n"
            msg += ":Total " + str(roll + modifyer) + "\n"
            msg += "```"
            await message.channel.send(msg)
            await message.delete()            
            
            
            
        if args[0] == prefix + "checkd":
            
            if len(args) == 1:
                modifyer = 0
                sign= "+"
                
            else:
            
                try: 
                    modifyer = int(args[1])
                    if modifyer > -1:
                       sign = "+"
                    else:
                        sign = "-"
                except:
                    return
                
            roll_1 = roll_dice(20)
            roll_2 = roll_dice(20)
            update_database(message.author.id, 20, roll_1)
            update_database(message.author.id, 20, roll_2)
            
            if roll_1 < roll_2:
                roll = roll_1
            else:
                roll = roll_2
            
            msg = "```css\n"
            msg += "{" + message.author.name + ": ' 1d20 " + sign + " " + str(abs(modifyer)) + " with disadvantage'}\n"
            msg += ":20 " + str(roll_1) + " " + str(roll_2) + "\n"
            msg += ":" + sign + str(abs(modifyer)) + " " + sign + str(abs(modifyer)) + "\n"
            msg += ":Total " + str(roll + modifyer) + "\n"
            msg += "```"
            await message.channel.send(msg)
            await message.delete()            
            
            
            
        
        if args[0] == prefix + "stats":
            
            try: 
                dice = int(args[1])
                db.check_dice(dice)
            except ValueError:
                await message.channel.send("Invalid dice size")
                return
            else:
                await message.channel.send("I don't think thats a number")
            
            if not db.check_table(dice) or not db.check_user(message.author.id, dice):
                await message.channel.send("Don't have data for this request")
                return
            
            # get users roll history
            rolls = db.get_rolls(message.author.id, dice)
    
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
            plt.title(message.author.name + " d" + str(dice) + " rolls")
            plt.ylabel("Frequency")
            plt.xlabel("Roll")
            
            # save image to send
            image_name = str(message.author.id)+"_d"+str(dice)+".png"
            plt.savefig(image_name)
            plt.clf()
            await message.channel.send(file=discord.File(image_name))
            await message.delete()
            os.remove(image_name)
            return
        
        
        
        if args[0] == prefix + "statsall":
            
            try:
                dice = int(args[1])
                db.check_dice(dice)
            except ValueError:
                await message.channel.send("Invalid dice size")
                return
            else:
                await message.channel.send("I don't think thats a number")
            
            rolls = rdb.get_all_rolls(message.author.id, dice)
        
            # make x coords
            x = []
            for i in range(1, dice+1):
                x.append(i)
            y = rolls[1:-1]
            
            # plot bar graph
            plt.bar(x, y, width = 1, color='blue', edgecolor='black')
            yint = range(min(y), math.ceil(max(y))+1)
            plt.yticks(yint)
            xint = range(1, dice+1)
            plt.xticks(xint)
            plt.title("all " + message.author.name + " d" + str(dice) + " rolls")
            plt.ylabel("Frequency")
            plt.xlabel("Roll")
            
            # save image to send
            image_name = str(message.author.id)+"_d"+str(dice)+".png"
            plt.savefig(image_name)
            plt.clf()
            await message.channel.send(file=discord.File(image_name))
            await message.delete()
            os.remove(image_name)
            return            
        
        
        
        if "maxbot" in message.content.lower() or "max bot" in message.content.lower():
            
            insult = [
                "Bellend",
                "Knobhead",
                "Fuck off",
                "Fuck you",
                "Prick",
                "Dickhead",
                "You have Herpes",
                "Nice cock",
                "Suck a fat one",
                "You bring everyone so much joy, when you leave the room.",
                "I think if you look at the facts, you'll find that incorrect",
                "I know you are but what am I?",
                "Cunt",
                "Wanker",
                "No you",
                "Bitch",
                
                      ]
            
            msg = insult[np.random.randint(len(insult))]
            await message.channel.send(msg)
        
        
        if args[0] == prefix + "test":
            
            #rolls = rdb.get_rolls(message.author.id, 20)
            
            await message.channel.send("/tts Discord's pretty awesome")
            await message.channel.send("/tts nice")
            await message.delete()
        
        
tok_file = open("token.txt", "r")
TOKEN = tok_file.readline()

client = MyClient()
client.run(TOKEN)