import discord
import commands


class MaxBot(discord.Client):

    # on bot start
    async def on_ready(self):
        print("Connected as {0.name} {0.id}".format(self.user))

    async def on_message(self, message):

        # print messages and users to console
        print("______________________________________________________")
        print("Msg: {}:".format(message.author.name))
        print("{}\n".format(message.content))

        # set command prefix
        prefix = "'"

        # check the message is a command and has content
        if not message.content or not message.content[0] == prefix:
            return

        # process message
        txt_cmd = commands.TextCommands(prefix, message)

        # executing this will return the message to send
        msg_out = txt_cmd.do()

        # if nothing is returned from error quit
        if msg_out is None:
            return

        # send response
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
