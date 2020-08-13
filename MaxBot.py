import discord
import commands


class MaxBot(discord.Client):

    # on bot start
    async def on_ready(self):
        print("Connected as {0.name} {0.id}".format(self.user))

    async def on_message(self, message):

        print("______________________________________________________")
        print("Msg: {}:".format(message.author.name))
        print("{}\n".format(message.content))

        # set command prefix
        prefix = "'"

        if not message.content or not message.content[0] == prefix:
            return

        txt_cmd = commands.TextCommands(message)
        msg_out = txt_cmd.do()

        if msg_out is None:
            return

        await message.channel.send(msg_out)
        await message.delete()


if __name__ == "__main__":
    # retrieve the token to log in
    tok_file = open("/home/pi/Documents/token.txt", "r")
    TOKEN = tok_file.readline()
    tok_file.close()

    # start maxbot
    client = MaxBot()
    client.run(TOKEN)
