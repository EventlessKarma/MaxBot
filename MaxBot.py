import discord
from discord.ext import commands
import roll_database as rdb
import maxbot_funcs
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import sqlite3

# sets matplotlib theme
plt.style.use('Solarize_Light2')
    
class MyClient(discord.Client):

    # on bot start
    async def on_ready(self):
        print('Connected!')
        print('Username: {0.name}\nID: {0.id}\n'.format(self.user))

    async def on_message(self, message):
        
        # set command prefix
        prefix = "'"

        # split up message into
        args = message.content.split(" ")
        
        # to quickly disconnect
        if message.content.startswith(prefix + "shutdown"):
            
            # only works under my id
            if message.author.id == 198783211776638976:
                await message.delete()
                await self.logout()
                await self.close()
        
        
        if args[0] == prefix + "roll":
            
            # passing all arguments here returns total roll and outcome of each argument
            roll, roll_msg = maxbot_funcs.bot_roll(message.author.id, args[1:])
            
            # discord message using code block
            msg = "```css\n" # language
            msg += "{" + message.author.name.replace(" ", "") + ": ' " # username

            # sends users command
            for i in args[1:]:
                msg += i + " "
            msg += "'}\n"    
            
            # loop over each argument and output response
            for i in range(len(args[1:])):
                msg += ":" + args[i+1] + " " + roll_msg[i] + "\n"
            
            # finally print total roll
            msg += ":Total " + str(roll) + "\n"
            
            # end code block
            msg += "```"
            
            # send response and delete users command
            await message.channel.send(msg)
            await message.delete()
            return
        

        # check command will roll 20 with modifier
        if args[0] == prefix + "check":
            
            # get the roll and the modifier
            roll, modifier = maxbot_funcs.checks_roll(message.author.id, args)
            
            # roll will be 0 if error occurs
            if roll == 0:
                await message.channel.send("Something wrong with that")

            # sign for message formatting
            if modifier < 0:
                sign = "-"
            else:
                sign = "+"    

            # message to send using code block format
            msg = "```css\n"
            msg += "{" + message.author.name.replace(" ", "") + ": ' 1d20 " + sign + " " + str(abs(modifier)) + " '}\n"
            msg += ":20 " + str(roll) + "\n"
            msg += ":" + sign + str(abs(modifier)) + " " + sign + str(abs(modifier)) + "\n"
            msg += ":Total " + str(roll + modifier) + "\n"
            msg += "```"
            await message.channel.send(msg)
            await message.delete()
            
        
        # checka command will roll 20 with advantage
        if args[0] == prefix + "checka":
            
            # get roll and modifier, advantage returns two rolls
            roll, modifier = maxbot_funcs.checks_roll(message.author.id, args, adv=True)
            
            # sign for message formatting
            if modifier < 0:
                sign = "-"
            else:
                sign = "+"

            # largest roll used in the total
            if roll[0] > roll[1]:
                adv = roll[0]
            else:
                adv = roll[1]
            
            # message to send using code block format
            msg = "```css\n"
            msg += "{" + message.author.name + ": ' 1d20 " + sign + " " + str(abs(modifier)) + " with advantage'}\n"
            msg += ":20 " + str(roll[0]) + " " + str(roll[1]) + "\n"
            msg += ":" + sign + str(abs(modifier)) + " " + sign + str(abs(modifier)) + "\n"
            msg += ":Total " + str(adv + modifier) + "\n"
            msg += "```"
            await message.channel.send(msg)
            await message.delete()            
            
            
        # 
        if args[0] == prefix + "checkd":
            
            # get roll and modifier, advantage returns two rolls
            roll, modifier = maxbot_funcs.checks_roll(message.author.id, args, adv=True)
            
            # sign for message formatting
            if modifier < 0:
                sign = "-"
            else:
                sign = "+"

            # smallest roll used in the total
            if roll[0] < roll[1]:
                adv = roll[0]
            else:
                adv = roll[1]
            
            # message to send using code block format
            msg = "```css\n"
            msg += "{" + message.author.name + ": ' 1d20 " + sign + " " + str(abs(modifier)) + " with disadvantage'}\n"
            msg += ":20 " + str(roll[0]) + " " + str(roll[1]) + "\n"
            msg += ":" + sign + str(abs(modifier)) + " " + sign + str(abs(modifier)) + "\n"
            msg += ":Total " + str(adv + modifier) + "\n"
            msg += "```"
            await message.channel.send(msg)
            await message.delete()            
            
        # stats command will send graph of current day's rolls
        if args[0] == prefix + "stats":
            
            # generate png graph
            image_name = maxbot_funcs.get_stats(message.author.name, message.author.id, args)

            # send graph and delete
            await message.channel.send(file=discord.File(image_name))
            await message.delete()
            os.remove(image_name)
            return
        
        
        # statsall command sends graph of all saved rolls
        if args[0] == prefix + "statsall":
            
            # generate png graph
            image_name = maxbot_funcs.get_stats(message.author.name, message.author.id, args, date="all")

            # send graph and delete
            await message.channel.send(file=discord.File(image_name))
            await message.delete()
            os.remove(image_name)
            return            
        
        
        # if maxbot is mentioned, insult the messenger 
        if "maxbot" in message.content.lower() or "max bot" in message.content.lower():
            
            # open the insults file
            try:
                fi = open("insults.txt")
            except:
                pass
            
            # get a random insult and send
            insult = maxbot_funcs.random_line(fi)
            await message.channel.send(insult)
        
        
        if args[0] == prefix + "test":
            conn = sqlite3.connect("../MaxBot_data/roll_data/2020-07-21.db")
            cur = conn.cursor()
            #cur.execute("SELECT * FROM d20")
            cur.execute("SELECT * FROM d20 WHERE user_id == {}".format(message.author.id))
            row = cur.fetchall()
            print(row)

# retrieve the token to log in
tok_file = open("../MaxBot_data/token.txt", "r")
TOKEN = tok_file.readline()

# start maxbot
client = MyClient()
client.run(TOKEN)
