import os
import discord
from discord.ext import commands
import minigames
from minigames import coinflip, help_cmd, highlow, rolladice, rps, scramble, trivia

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=['!'], intents=intents)

@client.event
async def on_ready():
    print('Gingery has connected to Discord!')
    
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening,name="!help"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Help Command
    if message.content.startswith('!help'):
        print("Help Command Executed by " + str(message.author))
        await help_cmd(message.channel)

    # Roll a Dice Command
    if message.content.startswith('!rolladice'):
        print("Rolladice Command Executed by " + str(message.author))
        await rolladice(message.channel)

    # Coin Flip Command
    if message.content.startswith('!coinflip'):
        print("Coinflip Command Executed by " + str(message.author))
        await coinflip(message.channel)

    # Rock Paper Scissors Command
    if message.content.startswith('!rps'):
        print("Rock Paper Scissors Command Executed by " + str(message.author))
        await rps(message.channel, message.content.split(' ')[1], message)

    # HighLow Command
    if message.content.startswith('!highlow'):
        print("HighLow Command Executed by " + str(message.author))
        await highlow(message.channel, message, client, message.author.mention)

    # Word Scramble Command 
    if message.content.startswith('!scramble'):
        print("Word Scramble Command Executed by " + str(message.author))
        await scramble(message.channel, message, client)

    # Trivia Game
    if message.content.startswith('!trivia'):
        print("Trivia Command Executed by " + str(message.author))
        await trivia(message.channel, message, client)

token = os.environ['TOKEN']
client.run(token)